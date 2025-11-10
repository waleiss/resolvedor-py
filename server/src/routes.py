from flask import request, jsonify
from src.parser import parse_expression
from src.controller import Controller
from src.services.gemini_service import GeminiService
from src.services.storage_service import StorageService
from run_solver import RULES
from run_evaluator import RULES_DICT

# Inicializa os serviços
gemini_service = GeminiService()
storage_service = StorageService()


def register_routes(app):
    """Registra todas as rotas da aplicação"""

    @app.route('/solvejson', methods=['POST'])
    def solve_problem_json():
        """
        Endpoint para resolver problemas de lógica proposicional.
        Recebe um JSON com sentenças e conclusão, e retorna o log de resolução.
        """
        try:
            # Recebendo dados do usuário
            data = request.json
            sentences = data.get("sentences", [])
            conclusion = data.get("conclusion", "")

            # Validando dados
            if not sentences or not conclusion:
                return jsonify({"error": "Sentenças e conclusão são obrigatórios"}), 400

            # Parseando sentenças e conclusão
            memory = [parse_expression(sentence) for sentence in sentences]
            conclusion_expr = parse_expression(conclusion)
            problem = 'Problema: ' + ', '.join([str(expr) for expr in memory]) + f' ⊢ {conclusion}'
            log = [problem]
            for expr in memory:
                log.append(f'({len(log)}) {expr}')
            log.append('---------------------------------------------------------')
            
            # Resolvendo o problema
            controller = Controller(RULES, memory, conclusion_expr, log)
            controller.run_solver()
            return jsonify({"log": log}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/evaluatejson', methods=['POST'])
    def evaluate_inferences_json():
        """
        Endpoint para avaliar inferências de lógica proposicional.
        Recebe um JSON com sentenças iniciais (premissas) e inferências,
        e retorna um log da avaliação.
        """
        try:
            # Recebendo dados do usuário
            data = request.json
            premises = data.get("premises", [])
            conclusion = data.get("conclusion", "")
            inferences = data.get("inferences", [])

            # Validando dados
            if not premises or not inferences or not conclusion:
                return jsonify({"error": "Premissas, conclusão e inferências são obrigatórias"}), 400
            
            # Parseando sentenças
            parsed_premises = [parse_expression(premise) for premise in premises]
            conclusion_expr = parse_expression(conclusion)
            log = []
            # Cria e executa o controlador
            controller = Controller(rules=RULES_DICT, memory=parsed_premises, conclusion=conclusion_expr, log=log)
            controller.run_evaluator(inferences=inferences)

            return jsonify({"log": log}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/solve', methods=['GET'])
    def solve_problem():
        """
        Endpoint para resolver problemas de lógica proposicional.
        Recebe um parâmetro de URL chamado 'frase' e retorna o log de resolução.
        """
        try:
            # Recebendo o parâmetro 'frase' da URL
            input_text = request.args.get("frase", "")

            # Validando o parâmetro
            if not input_text:
                return jsonify({"error": "O parâmetro 'frase' é obrigatório"}), 400

            # Processando a entrada
            try:
                # Separar as sentenças e a conclusão usando o delimitador "|"
                if "|" not in input_text:
                    return jsonify({"error": "Formato de entrada inválido. Use o delimitador '|' para separar sentenças e conclusão."}), 400
                
                sentences_part, conclusion_part = map(str.strip, input_text.split("|"))
                sentences = sentences_part.replace("sentenças:", "").strip()
                conclusion = conclusion_part.replace("conclusão:", "").strip()

                sentences = [sentence.strip() for sentence in sentences.split(",") if sentence.strip()]

            except Exception:
                return jsonify({"error": "Formato de entrada inválido. Use 'sentenças:' e 'conclusão:' separados por '|'"}), 400

            if not sentences or not conclusion:
                return jsonify({"error": "Sentenças e conclusão são obrigatórios"}), 400

            # Parseando sentenças e conclusão
            memory = [parse_expression(sentence) for sentence in sentences]
            conclusion_expr = parse_expression(conclusion)
            problem = 'Problema: ' + ', '.join([str(expr) for expr in memory]) + f' ⊢ {conclusion}'
            log = [problem]
            for expr in memory:
                log.append(f'({len(log)}) {expr}')
            log.append('---------------------------------------------------------')
            
            # Resolvendo o problema
            controller = Controller(RULES, memory, conclusion_expr, log)
            controller.run_solver()
            return jsonify({"log": log}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/evaluate', methods=['GET'])
    def evaluate_inferences():
        """
        Endpoint para avaliar inferências de lógica proposicional.
        Recebe um único parâmetro 'data' na URL, contendo premissas,
        conclusão e inferências em formato de string.
        """
        try:
            # Recebendo o parâmetro da URL
            data = request.args.get("data", "")

            if not data:
                return jsonify({"error": "O parâmetro 'data' é obrigatório"}), 400

            # Dividindo o texto em partes usando separadores conhecidos
            try:
                sections = data.split("|")
                premises_part = sections[0].replace("premissas:", "").strip()
                conclusion_part = sections[1].replace("conclusão:", "").strip()
                inferences_part = sections[2].replace("inferências:", "").strip()
            except IndexError:
                return jsonify({"error": "Formato inválido. Use 'premissas: ... | conclusão: ... | inferências: ...'"}), 400

            # Parseando as partes
            premises = [parse_expression(p.strip()) for p in premises_part.split(",")]
            conclusion = parse_expression(conclusion_part)
            inferences = [i.strip() for i in inferences_part.split(";")]

            # Validando os dados
            if not premises or not conclusion or not inferences:
                return jsonify({"error": "Premissas, conclusão e inferências são obrigatórias"}), 400

            # Criando o log
            log = []
            controller = Controller(rules=RULES_DICT, memory=premises, conclusion=conclusion, log=log)
            controller.run_evaluator(inferences=inferences)

            return jsonify({"log": log}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ========== NOVAS ROTAS PARA EXPERIMENTOS COM GEMINI ==========

    @app.route('/pipeline1', methods=['POST'])
    def solver_to_llm():
        """
        Endpoint para executar pipeline completo:
        1. Recebe o problema
        2. Resolve com o solver automático
        3. Envia para o Gemini avaliar
        4. Salva tudo em JSON (apenas se o Gemini responder com sucesso)
        """
        try:
            # Recebe dados
            data = request.json
            sentences = data.get("sentences", [])
            conclusion = data.get("conclusion", "")

            # Valida entrada
            if not sentences or not conclusion:
                return jsonify({"error": "Sentenças e conclusão são obrigatórios"}), 400

            # Passo 1: Resolve o problema
            memory = [parse_expression(sentence) for sentence in sentences]
            conclusion_expr = parse_expression(conclusion)
            problem = 'Problema: ' + ', '.join([str(expr) for expr in memory]) + f' ⊢ {conclusion}'
            log = [problem]
            for expr in memory:
                log.append(f'({len(log)}) {expr}')
            log.append('---------------------------------------------------------')
            
            controller = Controller(RULES, memory, conclusion_expr, log)
            controller.run_solver()

            # Passo 2: Envia para o Gemini avaliar
            gemini_evaluation = gemini_service.evaluate_solution(problem, log)

            # Verifica se o Gemini retornou erro
            if not gemini_evaluation.get("success", False):
                return jsonify({
                    "error": "Falha na avaliação do Gemini",
                    "solver_log": log,
                    "gemini_error": gemini_evaluation.get("error", "Erro desconhecido")
                }), 500

            # Passo 3: Salva os resultados (apenas se Gemini teve sucesso)
            save_result = storage_service.save_experiment_result(
                problem=problem,
                sentences=sentences,
                conclusion=conclusion,
                solver_log=log,
                gemini_evaluation=gemini_evaluation
            )

            if not save_result["success"]:
                return jsonify({
                    "warning": "Experimento executado mas não foi possível salvar",
                    "solver_log": log,
                    "gemini_evaluation": gemini_evaluation,
                    "save_error": save_result.get("error")
                }), 207  # Multi-Status

            # Retorna resultado completo
            return jsonify({
                "success": True,
                "solver_log": log,
                "gemini_evaluation": gemini_evaluation,
                "saved_to": save_result["filename"]
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/experiments', methods=['GET'])
    def list_experiments():
        """
        Lista todos os experimentos salvos.
        """
        try:
            experiments = storage_service.get_all_experiments()
            return jsonify({
                "success": True,
                "count": len(experiments),
                "experiments": experiments
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/experiments/<filename>', methods=['GET'])
    def get_experiment(filename):
        """
        Recupera um experimento específico pelo nome do arquivo.
        """
        try:
            result = storage_service.get_experiment(filename)
            
            if not result["success"]:
                return jsonify({"error": result["error"]}), 404
            
            return jsonify(result["data"]), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
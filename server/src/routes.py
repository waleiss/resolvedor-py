from flask import request, jsonify
from datetime import datetime
from typing import List, Dict, Any
from src.parser import parse_expression
from src.controller import Controller
from src.services.gemini_service import GeminiService
from src.services.storage_service import StorageService
from run_solver import RULES
from run_evaluator import RULES_DICT

# Inicializa os serviços
gemini_service = GeminiService()
storage_service = StorageService()


def _extract_solver_steps(log: List[str]) -> List[str]:
    """Extrai apenas as linhas de inferência do log do solver."""
    separator_index = -1
    for i, line in enumerate(log):
        if isinstance(line, str) and line.startswith('---'):
            separator_index = i
            break

    if separator_index >= 0:
        return [line for line in log[separator_index + 1:] if isinstance(line, str) and line.strip()]

    return [line for line in log if isinstance(line, str) and line.strip()]


def _build_problem_payload(problem: str, sentences: List[str], conclusion: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Monta o bloco problem no schema padrão."""
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return {
        "problem_id": data.get("problem_id") or f"problem_{timestamp_str}",
        "description": problem,
        "sentences": sentences,
        "conclusion": conclusion,
        "difficulty": data.get("difficulty", "medium")
    }


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
            gemini_evaluation = gemini_service.evaluate_solution(problem, _extract_solver_steps(log))

            # Verifica se o Gemini retornou erro
            if not gemini_evaluation.get("success", False):
                return jsonify({
                    "error": "Falha na avaliação do Gemini",
                    "solver_log": log,
                    "gemini_error": gemini_evaluation.get("error", "Erro desconhecido")
                }), 500

            # Passo 3: Monta documento no schema padrão e salva
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            doc_id = f"solver_to_llm_{timestamp_str}"

            experiment_document = {
                "_id": doc_id,
                "metadata": {
                    "timestamp": timestamp.isoformat(),
                    "pipeline": "solver_to_llm"
                },
                "problem": _build_problem_payload(problem, sentences, conclusion, data),
                "solver": {
                    "type": "agent_w",
                    "model": "solver"
                },
                "evaluator": {
                    "type": "llm",
                    "model": gemini_evaluation.get("model", "gemini-3-flash-preview")
                },
                "solver_output": {
                    "success": True,
                    "steps_raw": _extract_solver_steps(log)
                },
                "evaluation_output": {
                    "success": gemini_evaluation.get("success", False),
                    "log": gemini_evaluation.get("log")
                }
            }

            analysis_result = gemini_service.generate_structured_analysis(
                pipeline="solver_to_llm",
                problem_data=experiment_document["problem"],
                solver_output=experiment_document["solver_output"],
                evaluation_output=experiment_document["evaluation_output"],
            )
            experiment_document["analysis"] = analysis_result.get("analysis", None)

            save_result = storage_service.save_experiment_result(experiment_document)

            if not save_result["success"]:
                return jsonify({
                    "warning": "Experimento executado mas não foi possível salvar",
                    "experiment": experiment_document,
                    "save_error": save_result.get("error")
                }), 207  # Multi-Status

            # Retorna resultado completo
            return jsonify({
                "success": True,
                "experiment": experiment_document,
                "saved_to": save_result["filename"]
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/pipeline2', methods=['POST'])
    def llm_to_evaluator():
        """
        Endpoint para executar pipeline completo:
        1. Recebe o problema
        2. Gemini resolve o problema
        3. Avaliador verifica a solução do Gemini
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

            # Prepara o problema
            memory = [parse_expression(sentence) for sentence in sentences]
            conclusion_expr = parse_expression(conclusion)
            problem = 'Problema: ' + ', '.join([str(expr) for expr in memory]) + f' ⊢ {conclusion}'

            # Passo 1: Gemini resolve o problema
            gemini_solution = gemini_service.solve_problem(problem, sentences, conclusion)

            # Verifica se o Gemini retornou erro
            if not gemini_solution.get("success", False):
                return jsonify({
                    "error": "Falha ao solicitar solução do Gemini",
                    "gemini_error": gemini_solution.get("error", "Erro desconhecido")
                }), 500

            # Verifica se o Gemini retornou inferências
            inferences = gemini_solution.get("inferences", [])
            if not inferences:
                return jsonify({
                    "error": "Gemini não retornou inferências no formato esperado",
                    "gemini_solution": gemini_solution.get("solution", "")
                }), 422

            # Passo 2: Avaliador verifica a solução do Gemini
            log = []
            controller = Controller(rules=RULES_DICT, memory=memory, conclusion=conclusion_expr, log=log)
            controller.run_evaluator(inferences=inferences)

            # Passo 3: Monta documento no schema padrão e salva
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            doc_id = f"llm_to_eval_{timestamp_str}"

            experiment_document = {
                "_id": doc_id,
                "metadata": {
                    "timestamp": timestamp.isoformat(),
                    "pipeline": "llm_to_evaluator"
                },
                "problem": _build_problem_payload(problem, sentences, conclusion, data),
                "solver": {
                    "type": "llm",
                    "model": gemini_solution.get("model", "gemini-3-flash-preview")
                },
                "evaluator": {
                    "type": "agent_w",
                    "model": "evaluator"
                },
                "solver_output": {
                    "success": gemini_solution.get("success", False),
                    "steps_raw": gemini_solution.get("inferences", [])
                },
                "evaluation_output": {
                    "success": True,
                    "raw_text": None,
                    "log": log
                }
            }

            analysis_result = gemini_service.generate_structured_analysis(
                pipeline="llm_to_evaluator",
                problem_data=experiment_document["problem"],
                solver_output=experiment_document["solver_output"],
                evaluation_output=experiment_document["evaluation_output"],
            )
            experiment_document["analysis"] = analysis_result.get("analysis", None)

            save_result = storage_service.save_experiment_result(experiment_document)

            if not save_result["success"]:
                return jsonify({
                    "warning": "Experimento executado mas não foi possível salvar",
                    "experiment": experiment_document,
                    "save_error": save_result.get("error")
                }), 207  # Multi-Status

            # Retorna resultado completo
            return jsonify({
                "success": True,
                "experiment": experiment_document,
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

    @app.route('/experiments/full', methods=['GET'])
    def list_experiments_full():
        """
        Lista todos os experimentos com o documento completo, incluindo analysis.
        """
        try:
            experiments = storage_service.get_all_experiments_full()
            return jsonify({
                "success": True,
                "count": len(experiments),
                "experiments": experiments
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/experiments/evaluate", methods=["GET"])
    def list_experiments_evaluate():
        try:
            experiments = storage_service.get_experiments_evaluation()
            return jsonify({"success": True, "count": len(experiments), "experiments": experiments})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/experiments/<filename>/evaluate", methods=["POST"])
    def evaluate_experiment(filename):
        try:
            data = request.json
            evaluator = data.get("evaluator")
            clareza = data.get("clareza")
            justificativa = data.get("justificativa")
            consistencia = data.get("consistencia")
            if not evaluator or clareza is None or justificativa is None or consistencia is None:
                return jsonify({"success": False, "error": "Dados invalidos"}), 400
            result = storage_service.save_experiment_evaluation(filename, evaluator, clareza, justificativa, consistencia)
            if not result["success"]:
                return jsonify(result), 400
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

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
    
    @app.route('/problems', methods=['GET'])
    def list_problems():
        """
        Lista todos os problemas cadastrados.
        Query params opcionais:
        - difficulty: filtrar por dificuldade (easy, medium, hard)
        """
        try:
            # Pega o filtro opcional
            difficulty = request.args.get('difficulty')
            
            problems = storage_service.get_all_problems(difficulty=difficulty)
            
            return jsonify({
                "success": True,
                "count": len(problems),
                "problems": problems
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/problems', methods=['POST'])
    def add_problem():
        """
        Adiciona um novo problema ao banco de dados.
        Body JSON esperado:
        {
            "description": "p → q, p ⊢ q",
            "sentences": ["p → q", "p"],
            "conclusion": "q",
            "difficulty": "easy"  // opcional: easy, medium, hard (padrão: medium)
        }
        """
        try:
            data = request.json
            
            # Valida campos obrigatórios
            description = data.get("description")
            sentences = data.get("sentences")
            conclusion = data.get("conclusion")
            
            if not description or not sentences or not conclusion:
                return jsonify({
                    "error": "Campos obrigatórios: description, sentences, conclusion"
                }), 400
            
            # Campo opcional
            difficulty = data.get("difficulty", "medium")
            
            # Salva o problema
            result = storage_service.add_problem(
                description=description,
                sentences=sentences,
                conclusion=conclusion,
                difficulty=difficulty
            )
            
            if not result["success"]:
                return jsonify({"error": result["error"]}), 400
            
            return jsonify(result), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
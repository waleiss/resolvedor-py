from flask import Flask, request, jsonify
from flask_cors import CORS
from src.parser import parse_expression
from src.rules import *  # Todas as regras
from src.controller import Controller
from run_solver import RULES
from run_evaluator import RULES_DICT
from config import Config
app = Flask(__name__)
CORS(app)
# Inicialização do resolvedor e regras


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
        controller = Controller(rules=RULES_DICT, memory=parsed_premises, conclusion=conclusion_expr, log=log, gemini_api_key=Config.GEMINI_API_KEY)
        
        results  = controller.run_evaluator(inferences=inferences, premises_str=premises,
            conclusion_str=conclusion)

        feedback = None
        if results["invalid_inferences"] and controller.llm_feedback:
            feedback_result = controller.llm_feedback.generate_feedback(
                premises, conclusion, inferences, log
            )
            if feedback_result["status"] == "error":
                feedback = feedback_result["feedback"]
                
        return jsonify({
            "log": log,
            "results": results,
            "feedback": feedback,
            "success": len(results["invalid_inferences"]) == 0
        }), 200

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)

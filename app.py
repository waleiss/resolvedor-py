from flask import Flask, request, jsonify
from src.parser import parse_expression
from src.rules import *  # Todas as regras
from src.controller import Controller
from run_solver import RULES
from run_evaluator import RULES_DICT

app = Flask(__name__)

# Inicialização do resolvedor e regras


@app.route('/solve', methods=['POST'])
def solve_problem():
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


@app.route('/evaluate', methods=['POST'])
def evaluate_inferences():
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



if __name__ == '__main__':
    app.run(debug=True)

from src.controller import Controller
from src.rules import *  # Importa todas as regras
from src.expression import Expression
from src.parser import parse_expression

# simbolos = ['→', '↔', '¬', '∧', '∨']
# Regras
rules_dict = {
    "Silogismo Disjuntivo": DisjunctiveSyllogism(),
    "Modus Tollens": ModusTollens(),
    "Introdução da Bi-implicação": BiimplicationIntroduction(),
    "Dissociação de Bi-implicação": BiimplicationDissociation(),
    "Modus Ponens": ModusPonens(),
    "Silogismo Hipotético": HypotheticalSyllogism(),
    "Transposição": Transposition(),
    "Associatividade": Associativity(),
    "Comutatividade": Commutativity(),
    "Distributividade": Distributivity(),
    "De Morgan": DeMorgan(),
    "Dilema Construtivo": ConstructiveDilemma(),
    "Exportação": Exportation(),
    "Implicação Material": MaterialImplication(),
    "Conjunção": Conjunction(),
    "Simplificação": Simplification(),
    "Dupla Negação": DoubleNegation(),
    "Adição": Addition()
}


# Memória inicial

def initialize(premises, conclusion, inferences):

    print("\nDigite expressões no formato: '¬A', '(A ∨ B) → C', '¬(D ↔ E)'. Operadores válidos: ¬, ∨, ∧, →, ↔.",
          "\nQuando finalizar as premissas e quiser definir a conclusão, digite 'CONCLUSAO'.",
          "\nDepois da conclusão, você digitará seus passos de prova.",
          "\nCaso queira encerrar o programa, digite 'sair'.\n"
        )

    while True:
        user_input = input("Digite uma premissa (ou 'CONCLUSAO' para definir a conclusão): ").strip()
        if user_input.lower() == 'sair':
            print("Execução encerrada pelo usuário.")
            return None, None, None
        if user_input.lower() == 'conclusao':
            break
        
        try:
            expr = parse_expression(user_input)  # Converte string para Expression
            premises.append(expr)  # Adiciona à memória
            print(f"Premissa adicionada: {expr}")
        except Exception as e:
            print(f"Erro ao processar a premissa: {e}")

    while True:
        user_input = input("Digite a conclusão: ").strip()
        try:
            conclusion = parse_expression(user_input)
            print(f"Conclusão definida: {conclusion}")
            break
        except Exception as e:
            print(f"Erro ao processar a conclusão: {e}")

    while True:
        user_input = input("Digite uma inferência (ou 'TERMINAR' para encerrar sua prova): ").strip()
        if user_input.lower() == 'sair':
            print("Execução encerrada pelo usuário.")
            return None, None
        if user_input.lower() == 'terminar':
            break
        
        try:
            inferences.append(user_input)  # Adiciona à memória
            print(f"Inferência adicionada: {user_input}")
        except Exception as e:
            print(f"Erro ao processar a inferência: {e}") 
    
    return premises, conclusion, inferences

premises, conclusion, inferences = initialize(premises=[], conclusion=None, inferences=[])
if not premises or conclusion is None or not inferences:
    exit()

# Log de execução
log = []


# Cria e executa o controlador
controller = Controller(rules=rules_dict, memory=premises, conclusion=conclusion, log=log)
controller.run_evaluator(inferences=inferences)

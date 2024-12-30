from src.controller import Controller
from src.rules import *  # Importa todas as regras
from src.expression import Expression
from src.parser import parse_expression

# simbolos = ['→', '↔', '¬', '∧', '∨']
# Regras
rules = [
    DisjunctiveSyllogism(),
    ModusTollens(),
    BiimplicationIntroduction(),
    BiimplicationDissociation(),
    ModusPonens(),
    HypotheticalSyllogism(),
    Transposition(),
    Associativity(),
    Commutativity(),
    Distributivity(),
    DeMorgan(),
    ConstructiveDilemma(),
    Exportation(),
    MaterialImplication(),
    Conjunction(),
    Simplification(),
    DoubleNegation(),
    Addition(),
]

# Memória inicial

def initialize(memory, conclusion):

    print("\nDigite expressões no formato: '¬A', '(A ∨ B) → C', '¬(D ↔ E)'. Operadores válidos: ¬, ∨, ∧, →, ↔.",
          "\nQuando finalizar as premissas e quiser definir a conclusão, digite 'CONCLUIR'.",
          "\nCaso queira encerrar o programa, digite 'sair'.\n"
        )

    while True:
        user_input = input("Digite uma premissa (ou 'CONCLUIR' para definir a conclusão): ").strip()
        if user_input.lower() == 'sair':
            print("Execução encerrada pelo usuário.")
            return None, None
        if user_input.lower() == 'concluir':
            break
        
        try:
            expr = parse_expression(user_input)  # Converte string para Expression
            memory.append(expr)  # Adiciona à memória
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
    
    return memory, conclusion

memory, conclusion = initialize(memory=[], conclusion=None)
if not memory or conclusion is None:
    exit()

# Log de execução
problem = 'Problema: ' + ', '.join([str(expr) for expr in memory]) + f' ⊢ {conclusion}'
log = [problem]
for expr in memory:
    log.append(f'({len(log)}) {expr}')
log.append('---------------------------------------------------------')

# Cria e executa o controlador
controller = Controller(rules, memory, conclusion, log)
controller.run()

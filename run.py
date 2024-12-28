from src.controller import Controller
from src.rules import *  # Importa todas as regras
from src.expression import Expression

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
A = Expression(left="A")
B = Expression(left="B")
C = Expression(left="C")
implication = Expression(operator="→", left=A, right=B)
disjunction = Expression(operator='∨', left=B, right=C)
not_B = Expression(operator="¬", left=B)

memory = [implication, not_B, disjunction]
conclusion = Expression(operator="¬", left=A)

# Log de execução
problem = 'Problema: ' + ', '.join([str(expr) for expr in memory]) + f' ⊢ {conclusion}'
log = [problem]
for expr in memory:
    log.append(f'({len(log)}) {expr}')
log.append('---------------------------------------------------------')

# Cria e executa o controlador
controller = Controller(rules, memory, conclusion, log)
controller.run()

from src.controller import Controller
from src.rules import DisjunctiveSyllogism, ModusTollens, BiimplicationIntroduction, BiimplicationDissociation
from src.expression import Expression

# Regras
rules = [
    DisjunctiveSyllogism(),
    ModusTollens(),
    BiimplicationIntroduction(),
    BiimplicationDissociation()
]

# Memória inicial
A = Expression(left="A")
B = Expression(left="B")
C = Expression(left="C")
implication = Expression(operator="→", left=A, right=B)
disjunction= Expression(operator='∨', left=B,right=C)
not_B = Expression(operator="¬", left=B)
memory = [implication, not_B, disjunction ]

# Conclusão a ser provada
conclusion = Expression(operator="¬", left=A)

# Cria e executa o controlador
controller = Controller(rules, memory, conclusion)
controller.run()

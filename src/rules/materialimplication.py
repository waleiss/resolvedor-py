from ..interfaces import Observer
from ..expression import Expression

class MaterialImplication(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, new_expr):
        log.append(
            f"({len(log) - 1}) {new_expr}  Implicação Material  "
            f"{memory.index(expr) + 1}"
        )

    def update(self, memory, log):
        for expr in memory:
            # Verifica a forma P → Q
            if expr.operator == '→':
                antecedent = expr.left
                consequent = expr.right

                new_expr = Expression(
                    operator='∨',
                    left=Expression(operator='¬', left=antecedent, right=None),
                    right=consequent
                )

                if new_expr not in memory:
                    memory.append(new_expr)
                    self.add_to_log(log, memory, expr, new_expr)
                    print(f"Aplicando Implicação Material: {expr} ⇒ {new_expr}")
                    return
                
    def verify(self, memory):
        for expr in memory:
            # Verifica a possibilidade de P → Q
            if expr.operator == '→':
                antecedent = expr.left
                consequent = expr.right

                new_expr = Expression(
                    operator='∨',
                    left=Expression(operator='¬', left=antecedent, right=None),
                    right=consequent
                )

                if new_expr not in memory:
                    return True
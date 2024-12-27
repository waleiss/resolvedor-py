from ..interfaces import Observer
from ..expression import Expression

class MaterialImplication(Observer):
    def __init__(self):
        pass

    def is_negation(self, expression):
        return expression.operator == '¬'

    def get_negated(self, expression):
        if self.is_negation(expression):
            return expression.left  # Remove dupla negação
        return Expression(operator='¬', left=expression)

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

                negated_antecedent = self.get_negated(antecedent)

                new_expr = Expression(
                    operator='∨',
                    left=negated_antecedent,
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

                negated_antecedent = self.get_negated(antecedent)

                new_expr = Expression(
                    operator='∨',
                    left=negated_antecedent,
                    right=consequent
                )

                if new_expr not in memory:
                    return True
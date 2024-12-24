from ..interfaces import Observer
from ..expression import Expression

class Exportation(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for expr in memory:
            # Verifica a forma (P ∧ Q) → R
            if expr.operator == '→' and expr.left.operator == '∧':
                left_expr = expr.left.left
                right_expr = expr.left.right
                consequent = expr.right

                new_expr = Expression(
                    operator='→',
                    left=left_expr,
                    right=Expression(operator='→', left=right_expr, right=consequent)
                )

                if new_expr not in memory:
                    memory.append(new_expr)
                    print(f"Aplicando Exportação: {expr} ⇒ {new_expr}")
                    return

            # Verifica a forma P → (Q → R)
            if expr.operator == '→' and expr.right.operator == '→':
                antecedent = expr.left
                inner_antecedent = expr.right.left
                consequent = expr.right.right

                new_expr = Expression(
                    operator='→',
                    left=Expression(operator='∧', left=antecedent, right=inner_antecedent),
                    right=consequent
                )

                if new_expr not in memory:
                    memory.append(new_expr)
                    print(f"Aplicando Exportação: {expr} ⇒ {new_expr}")
                    return

    def verify(self, memory):
        for expr in memory:
            # Verifica a possibilidade de (P ∧ Q) → R
            if expr.operator == '→' and expr.left.operator == '∧':
                left_expr = expr.left.left
                right_expr = expr.left.right
                consequent = expr.right

                new_expr = Expression(
                    operator='→',
                    left=left_expr,
                    right=Expression(operator='→', left=right_expr, right=consequent)
                )

                if new_expr not in memory:
                    return True

            # Verifica a possibilidade de P → (Q → R)
            if expr.operator == '→' and expr.right.operator == '→':
                antecedent = expr.left
                inner_antecedent = expr.right.left
                consequent = expr.right.right

                new_expr = Expression(
                    operator='→',
                    left=Expression(operator='∧', left=antecedent, right=inner_antecedent),
                    right=consequent
                )

                if new_expr not in memory:
                    return True

        return False

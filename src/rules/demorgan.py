from ..interfaces import Observer
from ..expression import Expression

class DeMorgan(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  De Morgan  "
            f"{memory.index(expr) + 1}"
        )

    def is_negation(self, expression):
        return expression.operator == '¬'

    def get_negated(self, expression):
        if self.is_negation(expression):
            return expression.left
        return Expression(operator='¬', left=expression)

    def apply_de_morgan(self, operator, left_expr, right_expr):
        """
        Aplica a transformação de De Morgan com base no operador e subexpressões fornecidos.
        """
        negated_left = self.get_negated(left_expr)
        negated_right = self.get_negated(right_expr)
        new_operator = '∧' if operator == '∨' else '∨'
        return Expression(operator=new_operator, left=negated_left, right=negated_right)

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            if expr.operator == '¬' and expr.left.operator in ('∨', '∧'):
                inner_expr = expr.left
                transformed = self.apply_de_morgan(inner_expr.operator, inner_expr.left, inner_expr.right)

                if transformed not in memory:
                    memory.append(transformed)
                    print(f"Aplicando De Morgan: {expr} ⇒ {transformed}")
                    return

    def verify(self, memory, proposition):
        for expr in memory:
            if expr.operator == '¬' and expr.left.operator in ('∨', '∧'):
                inner_expr = expr.left
                transformed = self.apply_de_morgan(inner_expr.operator, inner_expr.left, inner_expr.right)

                if transformed not in memory and transformed == proposition:
                    return True

        return False

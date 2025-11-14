from ..interfaces import Observer
from ..expression import Expression

class DoubleNegation(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, simplified_expression):
        log.append(
            f"({len(log) - 1}) {simplified_expression}  Dupla Negação  "
            f"{memory.index(expr) + 1}"
        )

    def is_negation(self, expression):
        return expression.operator == '¬'

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            # Verifica se é uma negação e se o filho é uma negação também
            if self.is_negation(expr) and self.is_negation(expr.left):
                simplified_expression = expr.left.left
                if simplified_expression not in memory:
                    memory.append(simplified_expression)
                    self.add_to_log(log, memory, expr, simplified_expression)
                    print(f"Aplicando Dupla Negação: {expr} ⇒ {simplified_expression}")
                    return  # Adiciona apenas uma vez por iteração
            
            #Para E ↔ ¬(¬F) virar E ↔ F
            elif expr.operator and not self.is_negation(expr):
                new_expr = Expression(operator=expr.operator, left=expr.left, right=expr.right)
                if self.is_negation(expr.left) and self.is_negation(expr.left.left):
                    new_expr.left = expr.left.left.left
                if self.is_negation(expr.right) and self.is_negation(expr.right.left):
                    new_expr.right = expr.right.left.left
                if new_expr not in memory:
                    memory.append(new_expr)
                    self.add_to_log(log, memory, expr, new_expr)
                    print(f"Aplicando Dupla Negação: {expr} ⇒ {new_expr}")
                    return

    def verify(self, memory, proposition):
        for expr in memory:
            if self.is_negation(expr) and self.is_negation(expr.left):
                simplified_expression = expr.left.left
                if simplified_expression not in memory and simplified_expression == proposition:
                    return True
                
            elif expr.operator and not self.is_negation(expr):
                new_expr = Expression(operator=expr.operator, left=expr.left, right=expr.right)
                if self.is_negation(expr.left) and self.is_negation(expr.left.left):
                    new_expr.left = expr.left.left.left
                if self.is_negation(expr.right) and self.is_negation(expr.right.left):
                    new_expr.right = expr.right.left.left
                if new_expr not in memory and new_expr == proposition:
                    return True
        return False

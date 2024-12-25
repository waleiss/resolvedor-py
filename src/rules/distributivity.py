from ..interfaces import Observer
from ..expression import Expression

class Distributivity(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  Distributividade  "
            f"{memory.index(expr) + 1}"
        )

    def distribute(self, operator_outer, operator_inner, outer_expr, inner_left, inner_right):
        """
        Cria a expressão distribuída com base nos operadores e subexpressões fornecidos.
        """
        left_distributed = Expression(operator=operator_outer, left=outer_expr, right=inner_left)
        right_distributed = Expression(operator=operator_outer, left=outer_expr, right=inner_right)
        return Expression(operator=operator_inner, left=left_distributed, right=right_distributed)

    def update(self, memory, log):
        for expr in memory:
            if expr.operator == '∨' and expr.right.operator == '∧':
                # P ∨ (Q ∧ R) → (P ∨ Q) ∧ (P ∨ R)
                distributed = self.distribute('∨', '∧', expr.left, expr.right.left, expr.right.right)
                if distributed not in memory:
                    memory.append(distributed)
                    self.add_to_log(log, memory, expr, distributed)
                    print(f"Aplicando Distributividade: {expr} ⇒ {distributed}")
                    return

            if expr.operator == '∧' and expr.right.operator == '∨':
                # P ∧ (Q ∨ R) → (P ∧ Q) ∨ (P ∧ R)
                distributed = self.distribute('∧', '∨', expr.left, expr.right.left, expr.right.right)
                if distributed not in memory:
                    memory.append(distributed)
                    self.add_to_log(log, memory, expr, distributed)
                    print(f"Aplicando Distributividade: {expr} ⇒ {distributed}")
                    return

    def verify(self, memory):
        for expr in memory:
            if expr.operator == '∨' and expr.right.operator == '∧':
                distributed = self.distribute('∨', '∧', expr.left, expr.right.left, expr.right.right)
                if distributed not in memory:
                    return True

            if expr.operator == '∧' and expr.right.operator == '∨':
                distributed = self.distribute('∧', '∨', expr.left, expr.right.left, expr.right.right)
                if distributed not in memory:
                    return True

        return False

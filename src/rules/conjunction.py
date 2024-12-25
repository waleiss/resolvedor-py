from ..interfaces import Observer
from ..expression import Expression

class Conjunction(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, left_part, right_part, new_expr):
        log.append(
            f"({len(log) - 1}) {new_expr}  Conjunção  "
            f"{memory.index(left_part) + 1}, {memory.index(right_part) + 1}"
        )

    def update(self, memory, log):
        for expr in memory:
            # Verifica se existe uma sentença com conjunção na esquerda
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.left.operator == '∧':
                left_part = expr.left.left
                right_part = expr.left.right

                # Verifica se as partes da conjunção já estão isoladas na memória
                if left_part in memory and right_part in memory:
                    new_expr = Expression(operator='∧', left=left_part, right=right_part)
                    if new_expr not in memory:
                        memory.append(new_expr)
                        self.add_to_log(log, memory, left_part, right_part, new_expr)
                        print(f"Aplicando Conjunção: {left_part} e {right_part} ⇒ {new_expr}")
                        return

            # Verifica se existe uma sentença com conjunção na direita
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.right.operator == '∧':
                left_part = expr.right.left
                right_part = expr.right.right

                # Verifica se as partes da conjunção já estão isoladas na memória
                if left_part in memory and right_part in memory:
                    new_expr = Expression(operator='∧', left=left_part, right=right_part)
                    if new_expr not in memory:
                        memory.append(new_expr)
                        self.add_to_log(log, memory, left_part, right_part, new_expr)
                        print(f"Aplicando Conjunção: {left_part} e {right_part} ⇒ {new_expr}")
                        return

    def verify(self, memory):
        for expr in memory:
            # Verifica necessidade de conjunção na esquerda
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.left.operator == '∧':
                left_part = expr.left.left
                right_part = expr.left.right

                if left_part in memory and right_part in memory:
                    return True

            # Verifica necessidade de conjunção na direita
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.right.operator == '∧':
                left_part = expr.right.left
                right_part = expr.right.right

                if left_part in memory and right_part in memory:
                    return True

        return False

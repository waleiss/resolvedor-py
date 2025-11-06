from ..interfaces import Observer
from ..expression import Expression

class Associativity(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, associated):
        log.append(
            f"({len(log) - 1}) {associated}  Associatividade  "
            f"{memory.index(expr) + 1}"
        )

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            # Verifica se é do tipo P ∨ (Q ∨ R)
            if expr.operator == '∨' and expr.right.operator == '∨':
                left = expr.left
                middle = expr.right.left
                right = expr.right.right

                # Gera a forma associada: (P ∨ Q) ∨ R
                associated = Expression(operator='∨',
                                        left=Expression(operator='∨', left=left, right=middle),
                                        right=right)

                if associated not in memory:
                    memory.append(associated)
                    self.add_to_log(log, memory, expr, associated)
                    print(f"Aplicando Associatividade: {expr} ⇒ {associated}")
                    return

            # Verifica se é do tipo P ∧ (Q ∧ R)
            if expr.operator == '∧' and expr.right.operator == '∧':
                left = expr.left
                middle = expr.right.left
                right = expr.right.right

                # Gera a forma associada: (P ∧ Q) ∧ R
                associated = Expression(operator='∧',
                                        left=Expression(operator='∧', left=left, right=middle),
                                        right=right)

                if associated not in memory:
                    memory.append(associated)
                    self.add_to_log(log, memory, expr, associated)
                    print(f"Aplicando Associatividade: {expr} ⇒ {associated}")
                    return

    def verify(self, memory, proposition):
        for expr in memory:
            # Verifica se é do tipo P ∨ (Q ∨ R)
            if expr.operator == '∨' and expr.right.operator == '∨':
                left = expr.left
                middle = expr.right.left
                right = expr.right.right

                # Forma associada esperada: (P ∨ Q) ∨ R
                associated = Expression(operator='∨',
                                        left=Expression(operator='∨', left=left, right=middle),
                                        right=right)

                if associated not in memory and associated == proposition:
                    return True  # Regra pode ser aplicada

            # Verifica se é do tipo P ∧ (Q ∧ R)
            if expr.operator == '∧' and expr.right.operator == '∧':
                left = expr.left
                middle = expr.right.left
                right = expr.right.right

                # Forma associada esperada: (P ∧ Q) ∧ R
                associated = Expression(operator='∧',
                                        left=Expression(operator='∧', left=left, right=middle),
                                        right=right)

                if associated not in memory and associated == proposition:
                    return True  # Regra pode ser aplicada

        return False

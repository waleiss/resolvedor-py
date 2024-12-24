from ..interfaces import Observer
from ..expression import Expression

class Associativity(Observer):
    def __init__(self):
        pass

    def update(self, memory):
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
                    print(f"Aplicando Associatividade: {expr} ⇒ {associated}")
                    return

    def verify(self, memory):
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

                if associated not in memory:
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

                if associated not in memory:
                    return True  # Regra pode ser aplicada

        return False

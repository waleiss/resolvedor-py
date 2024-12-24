from ..interfaces import Observer
from ..expression import Expression

class Transposition(Observer):
    def __init__(self):
        pass

    def is_negation(self, expression):
        return expression.operator == '¬'

    def get_negated(self, expression):
        if self.is_negation(expression):
            return expression.left
        return Expression(operator='¬', left=expression)

    def update(self, memory):
        for expr in memory:
            if expr.operator == '→':  # Verifica implicação P → Q
                antecedent = expr.left
                consequent = expr.right

                # Gera a transposição: ¬Q → ¬P
                transposed = Expression(operator='→', left=self.get_negated(consequent), right=self.get_negated(antecedent))

                if transposed not in memory:
                    memory.append(transposed)
                    print(f"Aplicando Transposição: {expr} ⇒ {transposed}")
                    return  # Adiciona uma vez por iteração

    def verify(self, memory):
        for expr in memory:
            if expr.operator == '→':  # Verifica implicação P → Q
                antecedent = expr.left
                consequent = expr.right

                # Transposição esperada: ¬Q → ¬P
                transposed = Expression(operator='→', left=self.get_negated(consequent), right=self.get_negated(antecedent))

                if transposed not in memory:
                    return True  # Regra pode ser aplicada

        return False

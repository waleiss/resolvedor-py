from ..interfaces import Observer
from ..expression import Expression

class BiimplicationDissociation(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for expr in memory:
            # Procura por uma expressão do tipo A ↔ B
            if expr.operator == '↔':
                A = expr.left
                B = expr.right

                # Cria as novas implicações A → B e B → A
                implication1 = Expression(operator='→', left=A, right=B)
                implication2 = Expression(operator='→', left=B, right=A)

                # Adiciona as implicações na memória se não estiverem presentes
                added = False
                if implication1 not in memory:
                    memory.append(implication1)
                    print(f"Aplicando Dissociação de Bi-implicação: {expr} ⇒ {implication1}")
                    added = True
                if implication2 not in memory:
                    memory.append(implication2)
                    print(f"Aplicando Dissociação de Bi-implicação: {expr} ⇒ {implication2}")
                    added = True

                if added:
                    return  # Adiciona apenas uma vez por iteração

    def verify(self, memory):
        """Verifica se há uma bi-implicação dissociável na memória."""
        for expr in memory:
            if expr.operator == '↔':
                return True
        return False

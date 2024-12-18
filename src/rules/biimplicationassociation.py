from ..interfaces import Observer
from ..expression import Expression

class BiimplicationAssociation(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        # Procura por (A → B) e (B → A) na memória
        for expr1 in memory:
            if expr1.operator == '→':
                A = expr1.left
                B = expr1.right
                # Verifica se (B → A) também está na memória
                implication2 = Expression(operator='→', left=B, right=A)

                if implication2 in memory:
                    # Cria a bi-implicação (A ↔ B)
                    biimplication = Expression(operator='↔', left=A, right=B)

                    # Adiciona a bi-implicação na memória se não estiver presente
                    if biimplication not in memory:
                        memory.append(biimplication)
                        print(f"Aplicando Associação de Bi-implicação: {expr1} e {implication2} ⇒ {biimplication}")
                        return  # Adiciona apenas uma vez por iteração

    def verify(self, memory):
        """Verifica se há uma associação de bi-implicação aplicável na memória."""
        for expr1 in memory:
            if expr1.operator == '→':
                A = expr1.left
                B = expr1.right
                implication2 = Expression(operator='→', left=B, right=A)
                if implication2 in memory:
                    return True
        return False

from ..interfaces import Observer
from ..expression import Expression

class BiimplicationDissociation(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for expr in memory:
            # Forma 2 da Equivalencia Material: Procura por (A ↔ B) na memória para gerar (A → B) e (B → A)  
            if expr.operator == '↔':
                left = expr.left
                right = expr.right

                # Cria as novas implicações A → B e B → A
                implication1 = Expression(operator='→', left=left, right=right)
                implication2 = Expression(operator='→', left=right, right=left)

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
            # Forma 2 da Equivalencia Material: Procura por (A ↔ B) na memória para gerar (A → B) e (B → A) 
            if expr.operator == '↔':
                left = expr.left
                right = expr.right

                implication1 = Expression(operator='→', left=left, right=right)
                implication2 = Expression(operator='→', left=right, right=left)
                
                if implication1 not in memory or implication2 not in memory:
                    return True

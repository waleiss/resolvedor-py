from ..interfaces import Observer
from ..expression import Expression

class BiimplicationDissociation(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, implication):
        log.append(
            f"({len(log) - 1}) {implication}  Dissociação de Bi-implicação  "
            f"{memory.index(expr) + 1}"
        )

    def update(self, memory, log, conclusion=None):
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
                    self.add_to_log(log, memory, expr, implication1)
                    print(f"Aplicando Dissociação de Bi-implicação: {expr} ⇒ {implication1}")
                    added = True
                if implication2 not in memory:
                    memory.append(implication2)
                    self.add_to_log(log, memory, expr, implication2)
                    print(f"Aplicando Dissociação de Bi-implicação: {expr} ⇒ {implication2}")
                    added = True

                if added:
                    return  # Adiciona apenas uma vez por iteração

    def verify(self, memory, proposition):
        """Verifica se há uma bi-implicação dissociável na memória."""
        for expr in memory:
            # Forma 2 da Equivalencia Material: Procura por (A ↔ B) na memória para gerar (A → B) e (B → A) 
            if expr.operator == '↔':
                left = expr.left
                right = expr.right

                implication1 = Expression(operator='→', left=left, right=right)
                implication2 = Expression(operator='→', left=right, right=left)
                
                if implication1 not in memory or implication2 not in memory and proposition == implication1 or proposition == implication2:
                    return True

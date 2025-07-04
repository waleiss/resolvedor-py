from ..interfaces import Observer
from ..expression import Expression

class BiimplicationIntroduction(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, implication2, biimplication):
        log.append(
            f"({len(log) - 1}) {biimplication}  Introdução de Bi-implicação  "
            f"{memory.index(expr) + 1}, {memory.index(implication2) + 1}"
        )

    def update(self, memory, log, conclusion=None):

        for expr in memory:
            # Forma 1 da Equivalencia Material: Procura por (A → B) e (B → A) na memória para gerar (A ↔ B)
            if expr.operator == '→':
                left = expr.left
                right = expr.right
                # Verifica se (B → A) também está na memória
                implication2 = Expression(operator='→', left=right, right=left)

                if implication2 in memory:
                    # Cria a bi-implicação (A ↔ B)
                    biimplication = Expression(operator='↔', left=left, right=right)

                    # Adiciona a bi-implicação na memória se não estiver presente
                    if biimplication not in memory:
                        memory.append(biimplication)
                        self.add_to_log(log, memory, expr, implication2, biimplication)
                        print(f"Aplicando Associação de Bi-implicação: {expr} e {implication2} ⇒ {biimplication}")
                        return  # Adiciona apenas uma vez por iteração


    def verify(self, memory, proposition):
        """Verifica se há uma associação ou dissociação de bi-implicação aplicável na memória."""
        for expr in memory:

            # Forma 1 da Equivalencia Material: Procura por (A → B) e (B → A) na memória para gerar (A ↔ B)
            if expr.operator == '→':
                left = expr.left
                right = expr.right
                implication2 = Expression(operator='→', left=right, right=left)
                biimplication = Expression(operator='↔', left=left, right=right)

                if implication2 in memory and biimplication not in memory and biimplication == proposition:
                    return True
        
        return False

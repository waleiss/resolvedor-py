from ..interfaces import Observer
from ..expression import Expression

class DisjunctiveSyllogism(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, negative_disjunct, added_disjunct):
        log.append(
            f"({len(log) - 1}) {added_disjunct}  Silogismo Disjuntivo  "
            f"{memory.index(expr) + 1}, {memory.index(negative_disjunct) + 1}"
        )

    def is_negation(self, expression):
        """Verifica se uma expressão é do tipo ¬A."""
        return expression.operator == '¬'

    def get_negated(self, expression):
        """Retorna a expressão negada, garantindo estrutura correta."""
        if self.is_negation(expression):
            return expression.left  # ¬(¬A) → A
        return Expression(operator='¬', left=expression)

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            # Procura por uma expressão do tipo p ∨ q
            if expr.operator == '∨':
                disjunct1 = expr.left
                disjunct2 = expr.right

                negated_disjunct1 = self.get_negated(disjunct1)
                negated_disjunct2 = self.get_negated(disjunct2)

                if negated_disjunct1 in memory and disjunct2 not in memory:
                    memory.append(disjunct2)
                    self.add_to_log(log, memory, expr, negated_disjunct1, disjunct2)
                    print(f"Aplicando Silogismo Disjuntivo: {expr} e {negated_disjunct1} ⇒ {disjunct2}")
                    return
                
                if negated_disjunct2 in memory and disjunct1 not in memory:
                    memory.append(disjunct1)
                    self.add_to_log(log, memory, expr, negated_disjunct2, disjunct1)
                    print(f"Aplicando Silogismo Disjuntivo: {expr} e {negated_disjunct2} ⇒ {disjunct1}")
                    return
    
    def verify(self, memory, proposition):
        for expr in memory:
            if expr.operator == '∨':  # Se for uma disjunção
                disjunct1 = expr.left
                disjunct2 = expr.right

                # Verifica se a negação de um dos disjuntos está na memória
                negated_disjunct1 = self.get_negated(disjunct1)
                negated_disjunct2 = self.get_negated(disjunct2)

                if negated_disjunct1 in memory and disjunct2 not in memory and disjunct2 == proposition:
                    return True  # Regra pode ser aplicada gerando disjunct2
                if negated_disjunct2 in memory and disjunct1 not in memory and disjunct1 == proposition:
                    return True  # Regra pode ser aplicada gerando disjunct1

        return False  # Não encontrou condições para aplicar a regra

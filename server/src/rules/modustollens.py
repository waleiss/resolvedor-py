from ..interfaces import Observer
from ..expression import Expression

class ModusTollens(Observer):
    def __init__(self):
        pass

    def is_negation(self, expression):
        """Verifica se uma expressão é do tipo ¬A."""
        return expression.operator == '¬'

    def get_negated(self, expression):
        """Retorna a expressão negada, garantindo estrutura correta."""
        if self.is_negation(expression):
            return expression.left  # ¬(¬A) → A
        return Expression(operator='¬', left=expression)
    
    def add_to_log(self, log, memory, expr, negated_antecedent, negated_consequent):
        log.append(
            f"({len(log) - 1}) {negated_antecedent}  Modus Tollens  "
            f"{memory.index(expr) + 1}, {memory.index(negated_consequent) + 1}"
        )

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            # Procura por uma expressão do tipo A → B
            if expr.operator == '→':
                antecedent = expr.left
                consequent = expr.right

                # Verifica se a negação do consequente (¬B) está na memória
                negated_consequent = self.get_negated(consequent)
                if negated_consequent in memory:
                    # Se sim, adiciona a negação do antecedente (¬A) à memória
                    negated_antecedent = self.get_negated(antecedent)
                    if negated_antecedent not in memory:
                        memory.append(negated_antecedent)
                        self.add_to_log(log, memory, expr, negated_antecedent, negated_consequent)
                        print(f"Aplicando Modus Tollens: {expr} e {negated_consequent} ⇒ {negated_antecedent}")
                        return  # Adiciona apenas uma vez por iteração
    
    def verify(self, memory, proposition):
        for expr in memory:
            if expr.operator == '→':  # Se for uma implicação
                antecedent = expr.left
                consequent = expr.right

                # Verifica se a negação do consequente está na memória
                negated_consequent = self.get_negated(consequent)

                # Consequência esperada
                negated_antecedent = self.get_negated(antecedent)

                if negated_consequent in memory and negated_antecedent not in memory and negated_antecedent == proposition:
                    return True  # Regra pode ser aplicada gerando a negação do antecedente

        return False  # Não encontrou condições para aplicar a regra


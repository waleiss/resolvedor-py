from ..interfaces import Observer
from ..expression import Expression

class HypotheticalSyllogism(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for expr1 in memory:
            # Procura por uma expressão do tipo p → q
            if expr1.operator == '→':
                antecedent1 = expr1.left
                consequent1 = expr1.right

                for expr2 in memory:
                    # Procura por outra expressão do tipo q → r
                    if expr2.operator == '→' and expr2.left == consequent1:
                        antecedent2 = expr2.left
                        consequent2 = expr2.right

                        # Gera uma nova expressão condicional p → r
                        new_expression = Expression(operator='→', left=antecedent1, right=consequent2)

                        if new_expression not in memory:
                            memory.append(new_expression)
                            print(f"Aplicando Silogismo Hipotético: {expr1} e {expr2} ⇒ {new_expression}")
                            return  # Adiciona apenas uma vez por iteração
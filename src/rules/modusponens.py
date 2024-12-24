from ..interfaces import Observer
import re

class ModusPonens(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for expr in memory:
            # Procura por uma expressão do tipo A → B
            if expr.operator == '→':
                antecedent = expr.left
                consequent = expr.right

                # Verifica se o antecedente (A) está na memória
                if antecedent in memory:
                    # Se sim, adiciona o consequente (B) à memória, se ainda não estiver
                    if consequent not in memory:
                        memory.append(consequent)
                        print(f"Aplicando Modus Ponens: {antecedent} e {expr} ⇒ {consequent}")
                        return  # Adiciona apenas uma vez por iteração
                    
    def verify(self, memory):
        for expr in memory:
            # Procura por uma expressão do tipo A → B
            if expr.operator == '→':
                antecedent = expr.left
                consequent = expr.right

                # Verifica se o antecedente (A) está na memória
                if antecedent in memory:
                    # Se sim, adiciona o consequente (B) à memória, se ainda não estiver
                    if consequent not in memory:
                        return True
        return False
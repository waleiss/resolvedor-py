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
        atoms_alone = [atom for atom in memory if re.match(r'^[A-Z]$', atom)]
        atoms_with_implication = [atom for atom in memory if re.match(r'^[A-Z] → [A-Z]$', atom)]
        
        for implication in atoms_with_implication:
            if implication.split(' → ')[0] in atoms_alone and implication.split(' → ')[1] not in memory:
                return True
        
        return False
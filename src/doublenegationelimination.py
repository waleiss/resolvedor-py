from .interfaces import Observer
import re

class DoubleNegationElimination(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms_with_double_negation = [atom for atom in memory if re.match(r'^~~[A-Z]$', atom)]
        
        for double_negation in atoms_with_double_negation:
            if double_negation[2:] not in memory: #Verifica se o átomo sem a dupla negação não está na memória
                return memory.add(double_negation[2:])
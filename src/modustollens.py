from .interfaces import Observer
import re

class ModusTollens(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms_negation = [atom for atom in memory if re.match(r'^~[A-Z]$', atom)]
        atoms_with_implication = [atom for atom in memory if re.match(r'^[A-Z] → [A-Z]$', atom)]
        
        for implication in atoms_with_implication:
            if ('~'+ implication.split(' → ')[1]) in atoms_negation:
                return memory.add('~' + implication.split(' → ')[0])
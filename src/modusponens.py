from .interfaces import Observer
import re

class ModusPonens(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms_alone = [atom for atom in memory if re.match(r'^[A-Z]$', atom)]
        atoms_with_implication = [atom for atom in memory if re.match(r'^[A-Z] → [A-Z]$', atom)]
        
        for implication in atoms_with_implication:
            if implication.split(' → ')[0] in atoms_alone and implication.split(' → ')[1] not in memory:
                return memory.add(implication.split(' → ')[1])
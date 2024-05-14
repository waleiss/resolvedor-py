from .interfaces import Observer
import re

class HypotheticalSyllogism(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms_with_implication = [atom for atom in memory if re.match(r'^[A-Z] → [A-Z]$', atom)]
        
        for implication1 in atoms_with_implication:
            for implication2 in atoms_with_implication:
                if implication1.split(' → ')[1] == implication2.split(' → ')[0]:
                    new_implication = implication1.split(' → ')[0] + ' → ' + implication2.split(' → ')[1]
                    if new_implication not in memory:
                        return memory.add(new_implication)
from .interfaces import Observer
import re

class ConjunctionAssociation(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms = [atom for atom in memory if re.match(r'^[A-Z]$', atom)]
        
        for atom1 in atoms:
            for atom2 in atoms:
                if atom1 != atom2:
                    new_conjunction = atom1 + ' ∧ ' + atom2
                    if new_conjunction not in memory:
                        return memory.add(new_conjunction)
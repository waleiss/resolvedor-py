from .interfaces import Observer
import re

class ConjunctionDissociation(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms = [atom for atom in memory if re.match(r'^[A-Z]$', atom)]
        atoms_with_conjunction = [atom for atom in memory if re.match(r'^[A-Z] ∧ [A-Z]$', atom)]

        for atoms_conjunction in atoms_with_conjunction:
            if atoms_conjunction.split(' ∧ ')[0] not in memory and atoms_conjunction.split(' ∧ ')[1] not in memory:
                return memory.update(atoms_conjunction.split(' ∧ '))
            if atoms_conjunction.split(' ∧ ')[0] not in memory and atoms_conjunction.split(' ∧ ')[1] in memory:
                return memory.update(atoms_conjunction.split(' ∧ ')[0])
            if atoms_conjunction.split(' ∧ ')[0] in memory and atoms_conjunction.split(' ∧ ')[1] not in memory:
                return memory.update(atoms_conjunction.split(' ∧ ')[1])
from .interfaces import Observer
import re

class DisjunctiveSyllogism(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        atoms_negation = [atom for atom in memory if re.match(r'^~[A-Z]$', atom)]
        atoms_with_disjunction = [atom for atom in memory if re.match(r'^[A-Z] ∨ [A-Z]$', atom)]
        
        for disjunction in atoms_with_disjunction:
            if ('~'+ disjunction.split(' ∨ ')[0]) in atoms_negation:
                return memory.add(disjunction.split(' ∨ ')[1])
            elif ('~'+ disjunction.split(' ∨ ')[1]) in atoms_negation:
                return memory.add(disjunction.split(' ∨ ')[0])
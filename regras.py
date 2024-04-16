simbolos = ['→', '↔', '~', '∧', '∨']

class Regras:

    def ModusPonens(memoria):
        if 'P → Q' in memoria and 'P' in memoria:
            return memoria + ["Q"]
        else: 
            return memoria

    def ModusTollens(memoria):
        if 'P → Q' in memoria and '~Q' in memoria:
            return memoria + ["~P"]
        else: 
            return memoria
        
    def SilogismoHipotetico(memoria):
        if 'P → Q' in memoria and 'Q → R' in memoria:
            return memoria + ["P → R"]
        else: 
            return memoria

    def SilogismoDisjuntivo(memoria):
        if 'P ∨ Q' in memoria and '~P' in memoria:
            return memoria + ["Q"]
        elif 'P ∨ Q' in memoria and '~Q' in memoria:
            return memoria + ["P"]
        else: 
            return memoria
            
    def ElimDuplaNegacao(memoria):
        if '~~P' in memoria:
            return memoria + ["P"]
        else: 
            return memoria
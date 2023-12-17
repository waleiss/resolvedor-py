simbolos = ['→', '↔', '~', '∧', '∨']

def ModusPonens(estado):
    if 'P → Q' in estado and 'P' in estado:
        return estado + ["Q"]
    else: 
        return estado

def ModusTollens(estado):
    if 'P → Q' in estado and '~Q' in estado:
        return estado + ["~P"]
    else: 
        return estado
    
def SilogismoHipotetico(estado):
    if 'P → Q' in estado and 'Q → R' in estado:
        return estado + ["P → R"]
    else: 
        return estado

def SilogismoDisjuntivo(estado):
    if 'P ∨ Q' in estado and '~P' in estado:
        return estado + ["Q"]
    elif 'P ∨ Q' in estado and '~Q' in estado:
        return estado + ["P"]
    else: 
        return estado
        
def ElimDuplaNegacao(estado):
    if '~~P' in estado:
        return estado + ["P"]
    else: 
        return estado
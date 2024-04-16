from regras import Regras as regras
simbolos = ['→', '↔', '~', '∧', '∨']
#Separar a conclusão em uma variavel separada
#Fazer a memoria ser um set
memoria = ['P → Q', '~Q']
fim = '~P'
print(memoria)

while fim not in memoria:
    
    memoria = regras.ModusPonens(memoria)
    memoria = regras.ModusTollens(memoria)
    memoria = regras.SilogismoHipotetico(memoria)
    memoria = regras.SilogismoDisjuntivo(memoria)
    memoria = regras.ElimDuplaNegacao(memoria)
    
print(memoria)
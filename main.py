import regras
simbolos = ['→', '↔', '~', '∧', '∨']
#Separar a conclusão em uma variavel separada

estado = ['P → Q', 'P']
fim = 'Q'
print(estado)

estado = regras.ModusPonens(estado)
estado = regras.ModusTollens(estado)
estado = regras.SilogismoHipotetico(estado)
estado = regras.SilogismoDisjuntivo(estado)
estado = regras.ElimDuplaNegacao(estado)

print(estado)
from regras import Regras as regras

def aplicar_regra_e_verificar_memoria(regra, memoria, conclusao):
    memoria_anterior = memoria.copy()  # Faz uma cópia da memória antes da aplicação da regra
    memoria = regra(memoria)  # Aplica a regra na memória
    if conclusao in memoria:
        return memoria  # Se a conclusão desejada estiver na memória, retorna a memória atualizada
    elif memoria_anterior != memoria:
        return aplicar_regras(memoria, conclusao)  # Se houve mudança na memória, continua aplicando as regras
    else:
        return None  # Se não houve mudança na memória, retorna None, indicando que não é possível chegar à conclusão desejada

def aplicar_regras(memoria, conclusao, regras_module):
    regras = [
        regras_module.ModusPonens,
        regras_module.ModusTollens,
        regras_module.SilogismoHipotetico,
        regras_module.SilogismoDisjuntivo,
        regras_module.ElimDuplaNegacao
    ]
    for regra in regras:
        memoria_atualizada = aplicar_regra_e_verificar_memoria(regra, memoria, conclusao)
        if memoria_atualizada:
            return memoria_atualizada
    return None


simbolos = ['→', '↔', '~', '∧', '∨']
#Separar a conclusão em uma variavel separada
#Fazer a memoria ser um set
memoria = ['P → Q', '~Q']
conclusao = '~P'

resultado = aplicar_regras(memoria, conclusao, regras)
if resultado:
    print("Conclusão encontrada:", resultado)
else:
    print("Não foi possível chegar à conclusão desejada.")

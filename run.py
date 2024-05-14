from src import *

bb = BlackBoard()

mp = ModusPonens()
mt = ModusTollens()
hs = HypotheticalSyllogism()
ds = DisjunctiveSyllogism()
dne = DoubleNegationElimination()

memory = {'~~P', 'Y', 'R', 'S → T', '~Q'}
bb.subscribe(dne)
print(memory)
bb.notifyAll(memory)
print(memory)















""" simbolos = ['→', '↔', '~', '∧', '∨']

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


def aplicar_regra_e_verificar_memoria(regra, memoria, conclusao):
    memoria_anterior = memoria.copy()  # Faz uma cópia da memória antes da aplicação da regra
    memoria = regra(memoria)  # Aplica a regra na memória
    if conclusao in memoria and memoria_anterior != memoria:
        return memoria  # Se a conclusão desejada estiver na memória e houve mudança na memória, retorna a memória atualizada
    else:
        return None  # Caso contrário, retorna None, indicando que a memória não foi atualizada

def aplicar_regras(memoria, conclusao, regras_module):
    regras = [
        regras_module.ModusPonens,
        regras_module.ModusTollens,
        regras_module.SilogismoHipotetico,
        regras_module.SilogismoDisjuntivo,
        regras_module.ElimDuplaNegacao
    ]
    for regra in regras:
        resultado = aplicar_regra_e_verificar_memoria(regra, memoria, conclusao)
        if resultado:
            return resultado  # Retorna a memória atualizada se a conclusão desejada for encontrada e a memória for atualizada
    return memoria  # Retorna a memória sem alterações se nenhuma regra levar à conclusão desejada


simbolos = ['→', '↔', '~', '∧', '∨']
#Separar a conclusão em uma variavel separada
#Fazer a memoria ser um set
memoria = ['P → Q', '~Q']
conclusao = '~P'

resultado = aplicar_regras(memoria, conclusao, Regras)
if conclusao in resultado:
    print("Conclusão encontrada:", resultado)
else:
    print("Não foi possível chegar à conclusão desejada.")
 """
from src import *

bb = BlackBoard()
mp = ModusPonens()
mt = ModusTollens()
hs = HypotheticalSyllogism()
ds = DisjunctiveSyllogism()
dne = DoubleNegationElimination()

bb.subscribe(mp)
bb.subscribe(mt)
bb.subscribe(hs)
bb.subscribe(ds)
bb.subscribe(dne)

memory = {'P → Q', 'Q → S', 'S → R', 'P'}
goal = 'R'

while goal not in memory:
    memory_before = memory.copy()
    bb.notifyAll(memory)
    if memory == memory_before:
        break
    print(memory)

print('Conseguiu provar o argumento mostrando que', goal, 'é verdadeiro')
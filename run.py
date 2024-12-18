from src import *
from src.rules import *

# Criação do controlador
controller = Controller()

# Regras disponíveis
ds_rule = DisjunctiveSyllogism()
mt_rule = ModusTollens()

# Adiciona as regras ao controlador
controller.add_rule(ds_rule, priority=2)
controller.add_rule(mt_rule, priority=1)

# Define as premissas iniciais
P = Expression(left="P")
Q = Expression(left="Q")
not_P = Expression(operator="¬", left=P)
disjunction = Expression(operator="∨", left=P, right=Q)

controller.add_expression(disjunction)
controller.add_expression(not_P)

# Define a conclusão que queremos provar
controller.set_conclusion(Q)

# Executa o sistema
success = controller.execute()

# Logs de execução
for log in controller.get_logs():
    print(log)

# Resultado final
print("Conclusão foi alcançada:", success)
print("Memória final:", controller.get_memory())

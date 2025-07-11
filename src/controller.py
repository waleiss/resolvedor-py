import time
from .filter_steps import filter_relevant_steps
from .process_solution import process_inferences

class Controller:
    def __init__(self, rules, memory, conclusion, log):
        self.rules = rules  # Lista de regras (agentes)
        self.memory = memory  # Memória de trabalho compartilhada
        self.conclusion = conclusion  # Conclusão a ser provada
        self.log = log  # Log de execução

    def run_solver(self):
        """Executa todas as regras de forma sequencial."""
        print('')
        time_limit = 10
        start_time = time.time()

        while self.conclusion not in self.memory:
            # Verifica se o limite de tempo foi excedido
            if time.time() - start_time > time_limit:
                self.log.append("Tempo limite excedido. A conclusão não foi alcançada.")
                break
            # Tenta aplicar a regra
            for rule in self.rules:
                if self.conclusion not in self.memory:
                    rule.update(self.memory, self.log, self.conclusion)

        print('')
        # Exibe o log de execução
        for step in self.log:
            print(step)
        print('')

        print('Passos realmente relevantes:')
        # Exibe o log de execução
        passos = filter_relevant_steps(self.log, len(self.log) - 1)

        for step in self.log:
            if self.log.index(step) in passos:
                print(step)
        print('')

    def run_evaluator(self, inferences):
        
        process_inferences(inferences, self.rules, self.memory, self.log)
        print('\n')
        for step in self.log:
            print(step)
        print('')
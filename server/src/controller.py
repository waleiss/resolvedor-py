import time
from .filter_steps import filter_relevant_steps
from .process_solution import process_inferences

class Controller:
    def __init__(self, rules, memory, conclusion, log):
        self.rules = rules
        self.memory = memory
        self.conclusion = conclusion
        self.log = log
        self.full_log = []  # Log completo (opcional)

    def run_solver(self):
        """Executa todas as regras de forma sequencial."""
        print('')
        time_limit = 10
        start_time = time.time()

        while self.conclusion not in self.memory:
            if time.time() - start_time > time_limit:
                self.log.append("Tempo limite excedido. A conclusão não foi alcançada.")
                break
            for rule in self.rules:
                if self.conclusion not in self.memory:
                    rule.update(self.memory, self.log, self.conclusion)

        # Salva o log completo
        self.full_log = self.log.copy()
        
        print('')
        for step in self.full_log:
            print(step)
        print('')

        # Filtra e substitui pelo log relevante
        print('Passos realmente relevantes:')
        relevant_indices = filter_relevant_steps(self.log, len(self.log) - 1)
        self.log[:] = [step for i, step in enumerate(self.log) if i in relevant_indices]
        
        for step in self.log:
            print(step)
        print('')
    
    def run_evaluator(self, inferences):
        
        process_inferences(inferences, self.rules, self.memory, self.log, self.conclusion)
        print('\n')
        for step in self.log:
            print(step)
        print('')
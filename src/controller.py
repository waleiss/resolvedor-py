from time import sleep
from filter_steps import filter_relevant_steps

class Controller:
    def __init__(self, rules, memory, conclusion, log):
        self.rules = rules  # Lista de regras (agentes)
        self.memory = memory  # Memória de trabalho compartilhada
        self.conclusion = conclusion  # Conclusão a ser provada
        self.log = log  # Log de execução

    def run(self):
        """Executa todas as regras de forma sequencial."""
        print('')

        while self.conclusion not in self.memory:
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
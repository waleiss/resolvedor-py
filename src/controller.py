from time import sleep


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
                    print("Aplicando a regra:", rule.__class__.__name__)
                    print(self.memory)
                    rule.update(self.memory, self.log)
                    sleep(1)

        # Exibe o log de execução
        for step in self.log:
            print(step)
        print('')
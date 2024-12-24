import multiprocessing

class Controller:
    def __init__(self, rules, memory, conclusion):
        self.rules = rules  # Lista de regras (agentes)
        self.memory = multiprocessing.Manager().list(memory)  # Memória de trabalho compartilhada
        self.conclusion = conclusion  # Conclusão a ser provada
        #self.log = multiprocessing.Manager().list()  # Log de execução

    def agent_task(self, rule):
        """Tarefa de cada agente (regra)."""
        while True:
            if self.conclusion in self.memory:
                print(f"Conclusão '{self.conclusion}' alcançada! Memória final: {list(self.memory)}")
                return

            # Tenta aplicar a regra
            rule.update(self.memory)

    def run(self):
        """Executa todas as regras como agentes paralelos."""
        processes = []

        for rule in self.rules:
            process = multiprocessing.Process(target=self.agent_task, args=(rule,))
            processes.append(process)
            process.start()

        # Aguarda todos os processos terminarem (pararão quando a conclusão for alcançada)
        for process in processes:
            process.join()

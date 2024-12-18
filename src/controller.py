from typing import List, Tuple, Optional
from .interfaces import Observer
from .expression import Expression


class Controller:
    def __init__(self):
        self.memory: List[Expression] = []  # Memória de trabalho
        self.rules: List[Tuple[int, Observer]] = []  # Lista de regras com prioridade
        self.logs: List[str] = []  # Registro das execuções de regras
        self.conclusion: Optional[Expression] = None  # Conclusão-alvo

    def add_expression(self, expression: Expression):
        """Adiciona uma nova expressão ao estado compartilhado."""
        if expression not in self.memory:
            self.memory.append(expression)
            self.logs.append(f"Nova expressão adicionada: {expression}")

    def set_conclusion(self, conclusion: Expression):
        """Define a conclusão-alvo que o sistema deve tentar provar."""
        self.conclusion = conclusion
        self.logs.append(f"Conclusão definida: {conclusion}")

    def add_rule(self, rule: Observer, priority: int = 1):
        """Adiciona uma regra com uma prioridade específica."""
        self.rules.append((priority, rule))
        self.rules.sort(key=lambda x: x[0])  # Ordena por prioridade

    def remove_rule(self, rule: Observer):
        """Remove uma regra da lista de regras."""
        self.rules = [(p, r) for (p, r) in self.rules if r != rule]

    def execute(self):
        """Executa as regras aplicáveis até encontrar a conclusão ou esgotar as possibilidades."""
        if not self.conclusion:
            raise ValueError("Nenhuma conclusão foi definida.")

        while self.conclusion not in self.memory:
            applicable_rules = []

            # Identifica regras aplicáveis
            for _, rule in self.rules:
                if hasattr(rule, "verify") and rule.verify(self.memory):
                    applicable_rules.append(rule)

            if not applicable_rules:
                self.logs.append("Nenhuma regra aplicável encontrada. Conclusão não alcançada.")
                return False  # Falha ao provar a conclusão

            # Executa as regras aplicáveis
            for rule in applicable_rules:
                rule.update(self.memory)
                self.logs.append(f"Regra {rule.__class__.__name__} aplicada")

                # Verifica se a conclusão foi alcançada após a aplicação de cada regra
                if self.conclusion in self.memory:
                    self.logs.append(f"Conclusão alcançada: {self.conclusion}")
                    return True  # Sucesso ao provar a conclusão

        # Caso a conclusão já esteja na memória inicialmente
        self.logs.append(f"Conclusão já estava presente: {self.conclusion}")
        return True

    def get_logs(self) -> List[str]:
        """Retorna os logs de execução."""
        return self.logs

    def get_memory(self) -> List[Expression]:
        """Retorna o estado atual da memória compartilhada."""
        return self.memory

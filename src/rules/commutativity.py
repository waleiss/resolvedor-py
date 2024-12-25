from ..interfaces import Observer
from ..expression import Expression

class Commutativity(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, comuted_expr):
        log.append(
            f"({len(log) - 1}) {comuted_expr}  Comutatividade  "
            f"{memory.index(expr) + 1}"
        )

    def update(self, memory, log):
        for expr in memory:
            # Verifica se é uma conjunção ou disjunção
            if expr.operator in ['∧', '∨']:
                left = expr.left
                right = expr.right

                # Cria a expressão comutada
                commuted_expr = Expression(operator=expr.operator, left=right, right=left)

                # Adiciona à memória se ainda não estiver presente
                if commuted_expr not in memory:
                    memory.append(commuted_expr)
                    self.add_to_log(log, memory, expr, commuted_expr)
                    print(f"Aplicando Comutatividade: {expr} ⇒ {commuted_expr}")
                    return

    def verify(self, memory):
        for expr in memory:
            if expr.operator in ['∧', '∨']:
                left = expr.left
                right = expr.right

                # Cria a expressão comutada
                commuted_expr = Expression(operator=expr.operator, left=right, right=left)

                # Verifica se a comutada ainda não está na memória
                if commuted_expr not in memory:
                    return True  # Regra pode ser aplicada

        return False  # Não encontrou condições para aplicar a regra

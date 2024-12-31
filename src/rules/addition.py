from ..interfaces import Observer
from ..expression import Expression

class Addition(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, left_part, right_part, new_expr):
        indices = []
        #Pode ser que apenas uma parte da disjunção esteja na memória
        if left_part in memory:
            indices.append(str(memory.index(left_part) + 1))
        if right_part in memory:
            indices.append(str(memory.index(right_part) + 1))

        index_info = ", ".join(indices) if indices else ""

        log.append(
            f"({len(log) - 1}) {new_expr}  Adição  {index_info}"
        )

    def update(self, memory, log, conclusion=None):
        # Verifica a conclusão, caso seja fornecida
        if conclusion and conclusion.operator == '∨':
            left_part = conclusion.left
            right_part = conclusion.right

            # Verifica se ambas as partes estão na memória
            if left_part in memory or right_part in memory and conclusion not in memory:
                memory.append(conclusion)
                self.add_to_log(log, memory, left_part, right_part, conclusion)
                print(f"Aplicando Adição (Conclusão): {left_part} ∨ {right_part} ⇒ {conclusion}")
                return

        # Verifica as possibilidades na memória
        for expr in memory:
            # Procura por uma disjunção no lado esquerdo
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.left.operator == '∨':
                left_part = expr.left.left
                right_part = expr.left.right

                if left_part in memory or right_part in memory:
                    new_expr = Expression(operator='∨', left=left_part, right=right_part)
                    if new_expr not in memory:
                        memory.append(new_expr)
                        self.add_to_log(log, memory, left_part, right_part, new_expr)
                        print(f"Aplicando Adição: {left_part} ∨ {right_part} ⇒ {new_expr}")
                        return

            # Procura por uma disjunção no lado direito
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.right.operator == '∨':
                left_part = expr.right.left
                right_part = expr.right.right

                if left_part in memory or right_part in memory:
                    new_expr = Expression(operator='∨', left=left_part, right=right_part)
                    if new_expr not in memory:
                        memory.append(new_expr)
                        self.add_to_log(log, memory, left_part, right_part, new_expr)
                        print(f"Aplicando Adição: {left_part} ∨ {right_part} ⇒ {new_expr}")
                        return

    def verify(self, memory, proposition):
        # Verifica a conclusão, caso seja fornecida
        if proposition and proposition == '∨':
            left_part = proposition.left
            right_part = proposition.right

            if left_part in memory or right_part in memory:
                return True

        return False
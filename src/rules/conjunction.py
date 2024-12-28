from ..interfaces import Observer
from ..expression import Expression

class Conjunction(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, left_part, right_part, new_expr):
        log.append(
            f"({len(log) - 1}) {new_expr}  Conjunção  "
            f"{memory.index(left_part) + 1}, {memory.index(right_part) + 1}"
        )

    def update(self, memory, log, conclusion=None):
        # Primeiro, verifica se há necessidade de gerar a conclusão diretamente
        if conclusion and conclusion.operator == '∧':
            left_part = conclusion.left
            right_part = conclusion.right

            # Se ambas as partes estão na memória e a conclusão não foi formada
            if left_part in memory and right_part in memory and conclusion not in memory:
                memory.append(conclusion)
                self.add_to_log(log, memory, left_part, right_part, conclusion)
                print(f"Aplicando Conjunção (Conclusão): {left_part} e {right_part} ⇒ {conclusion}")
                return

        # Em seguida, verifica se há conjunções que podem ser formadas pela memória
        for expr in memory:
            # Verifica conjunções na esquerda
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.left.operator == '∧':
                left_part = expr.left.left
                right_part = expr.left.right

                if left_part in memory and right_part in memory:
                    new_expr = Expression(operator='∧', left=left_part, right=right_part)
                    if new_expr not in memory:
                        memory.append(new_expr)
                        self.add_to_log(log, memory, left_part, right_part, new_expr)
                        print(f"Aplicando Conjunção (Memória): {left_part} e {right_part} ⇒ {new_expr}")
                        return

            # Verifica conjunções na direita
            if expr.operator in ['→', '↔', '∧', '∨'] and expr.right.operator == '∧':
                left_part = expr.right.left
                right_part = expr.right.right

                if left_part in memory and right_part in memory:
                    new_expr = Expression(operator='∧', left=left_part, right=right_part)
                    if new_expr not in memory:
                        memory.append(new_expr)
                        self.add_to_log(log, memory, left_part, right_part, new_expr)
                        print(f"Aplicando Conjunção (Memória): {left_part} e {right_part} ⇒ {new_expr}")
                        return

    def verify(self, memory, conclusion=None):
        # Primeiro, verifica se a conclusão pode ser formada
        if conclusion and conclusion.operator == '∧':
            left_part = conclusion.left
            right_part = conclusion.right

            if left_part in memory and right_part in memory:
                return True

        # Em seguida, verifica conjunções que podem ser formadas pela memória
        for expr in memory:
            if expr.operator in ['→', '↔', '∧', '∨']:
                # Verifica necessidade de conjunção na esquerda
                if expr.left.operator == '∧':
                    left_part = expr.left.left
                    right_part = expr.left.right
                    if left_part in memory and right_part in memory:
                        new_expr = Expression(operator='∧', left=left_part, right=right_part)
                        if new_expr not in memory:
                            return True

                # Verifica necessidade de conjunção na direita
                if expr.right.operator == '∧':
                    left_part = expr.right.left
                    right_part = expr.right.right
                    if left_part in memory and right_part in memory:
                        new_expr = Expression(operator='∧', left=left_part, right=right_part)
                        if new_expr not in memory:
                            return True

        return False

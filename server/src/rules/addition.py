from ..interfaces import Observer
from ..expression import Expression

class Addition(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, left_part, right_part, new_expr):
        indices = []
        if left_part in memory:
            indices.append(str(memory.index(left_part) + 1))
        if right_part in memory:
            indices.append(str(memory.index(right_part) + 1))

        index_info = ", ".join(indices) if indices else ""

        log.append(
            f"({len(log) - 1}) {new_expr}  Adição  {index_info}"
        )

    def get_all_subexpressions(self, expr):
        """
        Coleta recursivamente todas as subexpressões de uma expressão.
        Isso serve como nosso 'radar' de necessidades.
        """
        subexprs = []
        if not hasattr(expr, 'operator'):
            return [expr]
        
        subexprs.append(expr)
        if hasattr(expr, 'left') and expr.left is not None:
            subexprs.extend(self.get_all_subexpressions(expr.left))
        if hasattr(expr, 'right') and expr.right is not None:
            subexprs.extend(self.get_all_subexpressions(expr.right))
        return subexprs

    def update(self, memory, log, conclusion=None):
        # 1. Mapeia todos os "alvos" (necessidades) em qualquer profundidade
        # da conclusão e de todas as expressões atualmente na memória
        targets = []
        if conclusion:
            targets.extend(self.get_all_subexpressions(conclusion))
        
        for expr in memory:
            targets.extend(self.get_all_subexpressions(expr))

        # 2. Para cada alvo encontrado, verifica se é uma disjunção
        # e se temos capacidade de construí-la agora
        for target in targets:
            if hasattr(target, 'operator') and target.operator == '∨':
                left_part = target.left
                right_part = target.right

                # Regra: Pelo menos um dos lados precisa estar solto na memória
                if left_part in memory or right_part in memory:
                    if target not in memory:
                        memory.append(target)
                        self.add_to_log(log, memory, left_part, right_part, target)
                        print(f"Aplicando Adição: {left_part} ∨ {right_part} ⇒ {target}")
                        return

    def verify(self, memory, proposition):
        if proposition and hasattr(proposition, 'operator') and proposition.operator == '∨':
            left_part = proposition.left
            right_part = proposition.right

            if left_part in memory or right_part in memory:
                return True

        return False
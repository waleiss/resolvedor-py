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

    def get_all_subexpressions(self, expr):
        """Coleta recursivamente todas as subexpressões para mapear necessidades."""
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
        # 1. Mapeia todos os "alvos" em qualquer profundidade
        targets = []
        if conclusion:
            targets.extend(self.get_all_subexpressions(conclusion))
        
        for expr in memory:
            targets.extend(self.get_all_subexpressions(expr))

        # 2. Varre os alvos em busca de necessidades de Conjunção (∧)
        for target in targets:
            if hasattr(target, 'operator') and target.operator == '∧':
                left_part = target.left
                right_part = target.right

                # Regra: AMBOS os lados precisam estar soltos na memória
                if left_part in memory and right_part in memory:
                    if target not in memory:
                        memory.append(target)
                        self.add_to_log(log, memory, left_part, right_part, target)
                        print(f"Aplicando Conjunção: {left_part} e {right_part} ⇒ {target}")
                        return

    def verify(self, memory, proposition):
        if proposition and hasattr(proposition, 'operator') and proposition.operator == '∧':
            left_part = proposition.left
            right_part = proposition.right

            if left_part in memory and right_part in memory:
                return True

        return False
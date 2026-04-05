from ..interfaces import Observer
from ..expression import Expression

class Exportation(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, new_expr):
        log.append(
            f"({len(log) - 1}) {new_expr}  Exportação  "
            f"{memory.index(expr) + 1}"
        )

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Exportação exatamente uma vez em qualquer profundidade.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        # --- 1. TENTATIVA NO NÍVEL ATUAL (Topo) ---
        if expr.operator == '→':
            # Via 1: (P ∧ Q) → R  ⇒  P → (Q → R)
            if hasattr(expr.left, 'operator') and expr.left.operator == '∧':
                p = expr.left.left
                q = expr.left.right
                r = expr.right

                transformations.append(
                    Expression(
                        operator='→',
                        left=p,
                        right=Expression(operator='→', left=q, right=r)
                    )
                )
                transformations.append(
                    Expression(
                        operator='→',
                        left=q,
                        right=Expression(operator='→', left=p, right=r)
                    )
                )

            # Via 2: P → (Q → R)  ⇒  (P ∧ Q) → R
            if hasattr(expr.right, 'operator') and expr.right.operator == '→':
                p = expr.left
                q = expr.right.left
                r = expr.right.right

                transformations.append(
                    Expression(
                        operator='→',
                        left=Expression(operator='∧', left=p, right=q),
                        right=r
                    )
                )

        # --- 2. RECURSÃO NOS FILHOS ---
        if hasattr(expr, 'left') and expr.left:
            for new_left in self.get_all_transformations(expr.left):
                transformations.append(
                    Expression(operator=expr.operator, left=new_left, right=getattr(expr, 'right', None))
                )

        if hasattr(expr, 'right') and expr.right:
            for new_right in self.get_all_transformations(expr.right):
                transformations.append(
                    Expression(operator=expr.operator, left=getattr(expr, 'left', None), right=new_right)
                )

        return transformations

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            for transformed in possiveis_transformacoes:
                if transformed not in memory:
                    memory.append(transformed)
                    self.add_to_log(log, memory, expr, transformed)
                    print(f"Aplicando Exportação: {expr} ⇒ {transformed}")
                    return

    def verify(self, memory, proposition):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
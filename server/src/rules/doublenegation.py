from ..interfaces import Observer
from ..expression import Expression

class DoubleNegation(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  Dupla Negação  "
            f"{memory.index(expr) + 1}"
        )

    def is_negation(self, expression):
        return hasattr(expression, 'operator') and expression.operator == '¬'

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Dupla Negação exatamente uma vez em qualquer profundidade.
        """
        transformations = []

        # --- 1. TENTATIVA NO NÍVEL ATUAL (Topo) ---
        
        # Via 1: ¬(¬P) ⇒ P (Remoção)
        if self.is_negation(expr) and self.is_negation(expr.left):
            transformations.append(expr.left.left)

        # Via 2: P ⇒ ¬(¬P) (Introdução)
        # Pode ser aplicado a qualquer expressão ou átomo (string)
        #transformations.append(
        #    Expression(operator='¬', left=Expression(operator='¬', left=expr))
        #)

        # --- 2. RECURSÃO NOS FILHOS ---
        # Só tenta recursão se expr for um objeto Expression (se for um átomo, pula isso)
        if hasattr(expr, 'operator'):
            if hasattr(expr, 'left') and expr.left is not None:
                for new_left in self.get_all_transformations(expr.left):
                    transformations.append(
                        Expression(operator=expr.operator, left=new_left, right=getattr(expr, 'right', None))
                    )

            if hasattr(expr, 'right') and expr.right is not None:
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
                    print(f"Aplicando Dupla Negação: {expr} ⇒ {transformed}")
                    return 

    def verify(self, memory, proposition):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
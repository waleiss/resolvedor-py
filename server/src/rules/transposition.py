from ..interfaces import Observer
from ..expression import Expression

class Transposition(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transposed):
        log.append(
            f"({len(log) - 1}) {transposed}  Transposição  "
            f"{memory.index(expr) + 1}"
        )

    def is_negation(self, expression):
        return expression.operator == '¬'

    def get_negated(self, expression):
        if self.is_negation(expression):
            return expression.left
        return Expression(operator='¬', left=expression)

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Transposição exatamente uma vez em qualquer profundidade.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        # --- 1. TENTATIVA NO NÍVEL ATUAL (Topo) ---
        # Via Única Universal: A → B  ⇒  ¬B → ¬A
        # Graças ao get_negated, isso já cobre o caminho inverso naturalmente.
        if expr.operator == '→':
            transformations.append(
                Expression(
                    operator='→', 
                    left=self.get_negated(expr.right), 
                    right=self.get_negated(expr.left)
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
                    print(f"Aplicando Transposição: {expr} ⇒ {transformed}")
                    return 

    def verify(self, memory, proposition):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
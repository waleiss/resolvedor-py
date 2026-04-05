from ..interfaces import Observer
from ..expression import Expression

class MaterialEquivalence(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  Equivalência Material  "
            f"{memory.index(expr) + 1}"
        )

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Equivalência Material exatamente uma vez em qualquer profundidade.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        # --- 1. TENTATIVA NO NÍVEL ATUAL (Topo) ---
        
        # Via 1: A ↔ B  ⇒  (A → B) ∧ (B → A)
        if expr.operator == '↔':
            left = expr.left
            right = expr.right
            transformations.append(
                Expression(
                    operator='∧',
                    left=Expression(operator='→', left=left, right=right),
                    right=Expression(operator='→', left=right, right=left)
                )
            )

        # Via 2: (A → B) ∧ (B → A)  ⇒  A ↔ B
        if expr.operator == '∧':
            if hasattr(expr.left, 'operator') and expr.left.operator == '→' and \
               hasattr(expr.right, 'operator') and expr.right.operator == '→':
                
                # Verifica se as implicações são cruzadas: left.left == right.right e left.right == right.left
                if expr.left.left == expr.right.right and expr.left.right == expr.right.left:
                    transformations.append(
                        Expression(
                            operator='↔',
                            left=expr.left.left,
                            right=expr.left.right
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
                    print(f"Aplicando Equivalência Material: {expr} ⇒ {transformed}")
                    return 

    def verify(self, memory, proposition):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
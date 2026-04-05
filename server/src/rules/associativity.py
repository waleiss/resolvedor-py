from ..interfaces import Observer
from ..expression import Expression

class Associativity(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, associated):
        log.append(
            f"({len(log) - 1}) {associated}  Associatividade  "
            f"{memory.index(expr) + 1}"
        )

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Associatividade exatamente uma vez em qualquer profundidade.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        # --- 1. TENTATIVA NO NÍVEL ATUAL (Topo) ---
        if expr.operator in ['∨', '∧']:
            op = expr.operator

            # Via 1: P op (Q op R) ⇒ (P op Q) op R
            if hasattr(expr.right, 'operator') and expr.right.operator == op:
                p = expr.left
                q = expr.right.left
                r = expr.right.right
                
                transformations.append(
                    Expression(operator=op,
                               left=Expression(operator=op, left=p, right=q),
                               right=r)
                )
                transformations.append(
                    Expression(operator=op,
                               left=Expression(operator=op, left=p, right=r),
                               right=q)
                )

            # Via 2: (P op Q) op R ⇒ P op (Q op R)
            if hasattr(expr.left, 'operator') and expr.left.operator == op:
                p = expr.left.left
                q = expr.left.right
                r = expr.right
                
                transformations.append(
                    Expression(operator=op,
                               left=p,
                               right=Expression(operator=op, left=q, right=r))
                )
                transformations.append(
                    Expression(operator=op,
                               left=q,
                               right=Expression(operator=op, left=p, right=r))
                )

        # --- 2. RECURSÃO NOS FILHOS ---
        # Tenta aplicar a regra dentro do lado esquerdo
        if hasattr(expr, 'left') and expr.left:
            for new_left in self.get_all_transformations(expr.left):
                transformations.append(
                    Expression(operator=expr.operator, left=new_left, right=getattr(expr, 'right', None))
                )

        # Tenta aplicar a regra dentro do lado direito
        if hasattr(expr, 'right') and expr.right:
            for new_right in self.get_all_transformations(expr.right):
                transformations.append(
                    Expression(operator=expr.operator, left=getattr(expr, 'left', None), right=new_right)
                )

        return transformations

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            # Pega todas as variações possíveis aplicando a regra 1 vez
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            for transformed in possiveis_transformacoes:
                if transformed not in memory:
                    memory.append(transformed)
                    self.add_to_log(log, memory, expr, transformed)
                    print(f"Aplicando Associatividade: {expr} ⇒ {transformed}")
                    return 

    def verify(self, memory, proposition):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
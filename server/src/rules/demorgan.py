from ..interfaces import Observer
from ..expression import Expression

class DeMorgan(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  De Morgan  "
            f"{memory.index(expr) + 1}"
        )

    def is_negation(self, expression):
        return expression.operator == '¬'

    def get_negated(self, expression):
        # Se for ¬P, retorna P. Se for P, retorna ¬P.
        if self.is_negation(expression):
            return expression.left
        return Expression(operator='¬', left=expression)

    def transform_recursive(self, expr):
        if not hasattr(expr, 'operator'):
            return expr

        # --- TENTATIVA DE APLICAÇÃO NO NÍVEL ATUAL (Mão Dupla) ---
        
        # VIA 1: ¬(A ∨ B)  =>  ¬A ∧ ¬B  (Distribuição da negação)
        if expr.operator == '¬' and hasattr(expr.left, 'operator') and expr.left.operator in ('∨', '∧'):
            inner = expr.left
            return self.apply_de_morgan(inner.operator, inner.left, inner.right, mode=1)

        # VIA 2: (A ∨ B)   =>  ¬(¬A ∧ ¬B) (Universalidade/Inversão)
        if expr.operator in ('∨', '∧'):
            return self.apply_de_morgan(expr.operator, expr.left, expr.right, mode=2)

        # --- RECURSÃO NOS FILHOS ---
        if hasattr(expr, 'left') and expr.left:
            new_left = self.transform_recursive(expr.left)
            if new_left != expr.left:
                return Expression(operator=expr.operator, left=new_left, right=getattr(expr, 'right', None))
                
        if hasattr(expr, 'right') and expr.right:
            new_right = self.transform_recursive(expr.right)
            if new_right != expr.right:
                return Expression(operator=expr.operator, left=expr.left, right=new_right)

        return expr

    def apply_de_morgan(self, operator, left_expr, right_expr, mode):
        # Inverte o operador principal
        new_operator = '∧' if operator == '∨' else '∨'
        
        # Inverte o sinal dos termos internos usando sua lógica universal
        neg_left = self.get_negated(left_expr)
        neg_right = self.get_negated(right_expr)

        if mode == 1:
            # ¬(A v B) -> (¬A ^ ¬B)
            return Expression(operator=new_operator, left=neg_left, right=neg_right)
        else:
            # (A v B) -> ¬(¬A ^ ¬B)
            inner = Expression(operator=new_operator, left=neg_left, right=neg_right)
            return Expression(operator='¬', left=inner)

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        De Morgan exatamente uma vez em qualquer subexpressão de 'expr'.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        # --- TENTATIVA DE APLICAÇÃO NO NÍVEL ATUAL ---
        # Via 1: ¬(A ∨ B)  =>  ¬A ∧ ¬B
        if expr.operator == '¬' and hasattr(expr.left, 'operator') and expr.left.operator in ('∨', '∧'):
            inner = expr.left
            transformations.append(self.apply_de_morgan(inner.operator, inner.left, inner.right, mode=1))

        # Via 2: (A ∨ B)   =>  ¬(¬A ∧ ¬B)
        if expr.operator in ('∨', '∧'):
            transformations.append(self.apply_de_morgan(expr.operator, expr.left, expr.right, mode=2))

        # --- RECURSÃO NOS FILHOS ---
        if hasattr(expr, 'left') and expr.left:
            # Para cada transformação possível no lado esquerdo, reconstrói a árvore principal
            for new_left in self.get_all_transformations(expr.left):
                transformations.append(Expression(operator=expr.operator, left=new_left, right=getattr(expr, 'right', None)))
                
        if hasattr(expr, 'right') and expr.right:
            # Para cada transformação possível no lado direito, reconstrói a árvore principal
            for new_right in self.get_all_transformations(expr.right):
                transformations.append(Expression(operator=expr.operator, left=expr.left, right=new_right))

        return transformations

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            transformed = self.transform_recursive(expr)
        
            if transformed != expr and transformed not in memory:
                memory.append(transformed)
                self.add_to_log(log, memory, expr, transformed)
                print(f"Aplicando De Morgan: {expr} ⇒ {transformed}")
                return

    def verify(self, memory, proposition):
        # Verifica se a proposição do aluno corresponde a ALGUMA das transformações
        # possíveis em qualquer nível de profundidade das expressões em memória.
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            # Requer que o método __eq__ da classe Expression esteja implementado corretamente
            if proposition in possiveis_transformacoes:
                return True
                
        return False
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
        if self.is_negation(expression):
            return expression.left
        return Expression(operator='¬', left=expression)

    def transform_recursive(self, expr):
        # Caso Base: se não for uma expressão (ex: átomo string), retorna ela mesma
        if not hasattr(expr, 'operator'):
            return expr

        # 1. Tenta aplicar De Morgan no nível ATUAL
        # Caso A: ¬(A ∨ B) ou ¬(A ∧ B)
        if expr.operator == '¬' and hasattr(expr.left, 'operator') and expr.left.operator in ('∨', '∧'):
            inner = expr.left
            return self.apply_de_morgan(inner.operator, inner.left, inner.right, 1)

        # 2. Se não aplicou no topo, tenta aplicar nos FILHOS (Recursão)
        if expr.operator in ('∨', '∧', '→'):
            new_left = self.transform_recursive(expr.left)
            # Se o lado esquerdo mudou, retornamos a nova versão da árvore
            if new_left != expr.left:
                return Expression(operator=expr.operator, left=new_left, right=expr.right)
                
            new_right = self.transform_recursive(expr.right)
            # Se o lado direito mudou, retornamos a nova versão
            if new_right != expr.right:
                return Expression(operator=expr.operator, left=expr.left, right=new_right)

        return expr # Nenhuma transformação possível neste ramo

    def apply_de_morgan(self, operator, left_expr, right_expr, mode):
        """
        Aplica a transformação de De Morgan com base no operador e subexpressões fornecidos.
        """
        match mode:
            case 1:
                negated_left = self.get_negated(left_expr)
                negated_right = self.get_negated(right_expr)
                new_operator = '∧' if operator == '∨' else '∨'
                return Expression(operator=new_operator, left=negated_left, right=negated_right)
           
            case 2:
                negated_left = self.get_negated(left_expr)
                negated_right = self.get_negated(right_expr)
                new_operator = '∧' if operator == '∨' else '∨'
                new_inner = Expression(operator=new_operator, left=negated_left, right=negated_right)
                return Expression(operator='¬', left=new_inner)
    

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            transformed = self.transform_recursive(expr)
        
            if transformed != expr and transformed not in memory:
                memory.append(transformed)
                self.add_to_log(log, memory, expr, transformed)
                print(f"Aplicando De Morgan Recursivo: {expr} ⇒ {transformed}")
                return # Para o loop para processar a nova sentença na próxima iteração

    def verify(self, memory, proposition):
        for expr in memory:
            if expr.operator == '¬' and expr.left.operator in ('∨', '∧'):
                inner_expr = expr.left
                transformed = self.apply_de_morgan(inner_expr.operator, inner_expr.left, inner_expr.right, 1)

                if transformed not in memory and transformed == proposition:
                    return True

            elif expr.operator in ('∨', '∧'):
                transformed = self.apply_de_morgan(expr.operator, expr.left, expr.right, 2)
                
                if transformed not in memory and transformed == proposition:
                    return True  
        return False

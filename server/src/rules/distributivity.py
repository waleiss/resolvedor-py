from ..interfaces import Observer
from ..expression import Expression

class Distributivity(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  Distributividade  "
            f"{memory.index(expr) + 1}"
        )

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Distributividade (ida ou volta) exatamente uma vez em qualquer profundidade.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        if expr.operator in ['∨', '∧']:
            op_main = expr.operator
            op_sub = '∧' if op_main == '∨' else '∨'

            # ==========================================
            # VIA 1: DISTRIBUIR (Expandir)
            # ==========================================
            
            # Caso 1A: Termo à esquerda -> P op_main (Q op_sub R)
            if hasattr(expr.right, 'operator') and expr.right.operator == op_sub:
                p = expr.left
                q = expr.right.left
                r = expr.right.right
                
                # Gera: (P op_main Q) op_sub (P op_main R)
                transformations.append(
                    Expression(operator=op_sub,
                               left=Expression(operator=op_main, left=p, right=q),
                               right=Expression(operator=op_main, left=p, right=r))
                )

            # Caso 1B: Termo à direita -> (Q op_sub R) op_main P
            if hasattr(expr.left, 'operator') and expr.left.operator == op_sub:
                q = expr.left.left
                r = expr.left.right
                p = expr.right
                
                # Gera: (Q op_main P) op_sub (R op_main P)
                transformations.append(
                    Expression(operator=op_sub,
                               left=Expression(operator=op_main, left=q, right=p),
                               right=Expression(operator=op_main, left=r, right=p))
                )

            # ==========================================
            # VIA 2: FATORAR (Colocar em evidência)
            # ==========================================
            
            # Precisamos de uma estrutura: (A op_sub B) op_main (C op_sub D)
            if (hasattr(expr.left, 'operator') and expr.left.operator == op_sub and
                hasattr(expr.right, 'operator') and expr.right.operator == op_sub):
                
                A = expr.left.left
                B = expr.left.right
                C = expr.right.left
                D = expr.right.right

                # Caso 2A: Termo em comum está à esquerda (A == C)
                # Ex: (P v Q) ^ (P v R) => P v (Q ^ R)
                if A == C:
                    transformations.append(
                        Expression(operator=op_sub,
                                   left=A,
                                   right=Expression(operator=op_main, left=B, right=D))
                    )
                
                # Caso 2B: Termo em comum está à direita (B == D)
                # Ex: (Q v P) ^ (R v P) => (Q ^ R) v P
                elif B == D:
                    transformations.append(
                        Expression(operator=op_sub,
                                   left=Expression(operator=op_main, left=A, right=C),
                                   right=B)
                    )
                
                # (Nota: Se o aluno tiver (P v Q) ^ (R v P), a comutatividade 
                # cuidará de alinhar isso antes de cair aqui).

        # --- RECURSÃO NOS FILHOS ---
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
                    print(f"Aplicando Distributividade: {expr} ⇒ {transformed}")
                    return 

    def verify(self, memory, proposition):
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
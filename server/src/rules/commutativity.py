from ..interfaces import Observer
from ..expression import Expression

class Commutativity(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, transformed):
        log.append(
            f"({len(log) - 1}) {transformed}  Comutatividade  "
            f"{memory.index(expr) + 1}"
        )

    def get_all_transformations(self, expr):
        """
        Retorna uma lista de todas as expressões possíveis geradas ao aplicar
        a Comutatividade exatamente uma vez em qualquer profundidade.
        """
        if not hasattr(expr, 'operator'):
            return []

        transformations = []

        # --- 1. TENTATIVA NO NÍVEL ATUAL (Topo) ---
        # A ∧ B => B ∧ A  |  A ∨ B => B ∨ A
        # Nota: Se o seu sistema tiver bi-implicação '↔', você pode adicionar à lista ['∧', '∨', '↔']
        if expr.operator in ['∧', '∨', '↔']:
            transformations.append(
                Expression(operator=expr.operator, left=expr.right, right=expr.left)
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
            # Pega todas as variações possíveis comutando 1 vez em qualquer lugar
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            for transformed in possiveis_transformacoes:
                # O motor aplica a PRIMEIRA transformação que for inédita
                if transformed not in memory:
                    memory.append(transformed)
                    self.add_to_log(log, memory, expr, transformed)
                    print(f"Aplicando Comutatividade: {expr} ⇒ {transformed}")
                    return # Para o loop para o motor processar o novo passo

    def verify(self, memory, proposition):
        # A avaliação fica elegante e exata: a resposta do aluno está
        # contida nas transformações válidas?
        for expr in memory:
            possiveis_transformacoes = self.get_all_transformations(expr)
            
            if proposition in possiveis_transformacoes:
                return True
                
        return False
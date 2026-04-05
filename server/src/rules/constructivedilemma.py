from ..interfaces import Observer
from ..expression import Expression

class ConstructiveDilemma(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, premises, new_disjunction):
        # Transforma a lista de premissas em seus respectivos índices na memória
        indices = [str(memory.index(p) + 1) for p in premises]
        log.append(
            f"({len(log) - 1}) {new_disjunction}  Dilema Construtivo  {', '.join(indices)}"
        )

    def update(self, memory, log, conclusion=None):
        # 1. Tenta a forma padrão de 3 premissas: A → B, C → D, A ∨ C
        for imp1 in memory:
            if hasattr(imp1, 'operator') and imp1.operator == '→':
                for imp2 in memory:
                    if hasattr(imp2, 'operator') and imp2.operator == '→' and imp1 != imp2:
                        for disj in memory:
                            if hasattr(disj, 'operator') and disj.operator == '∨' and \
                               (imp1.left == disj.left) and (imp2.left == disj.right):
                                
                                new_disjunction = Expression(operator='∨', left=imp1.right, right=imp2.right)

                                if new_disjunction not in memory:
                                    memory.append(new_disjunction)
                                    self.add_to_log(log, memory, [imp1, imp2, disj], new_disjunction)
                                    print(f"Aplicando Dilema Construtivo: {imp1}, {imp2}, {disj} ⇒ {new_disjunction}")
                                    return

        # 2. Tenta a forma de 2 premissas: (A → B) ∧ (C → D), A ∨ C
        for conj in memory:
            if hasattr(conj, 'operator') and conj.operator == '∧':
                if hasattr(conj.left, 'operator') and conj.left.operator == '→' and \
                   hasattr(conj.right, 'operator') and conj.right.operator == '→':
                    for disj in memory:
                        if hasattr(disj, 'operator') and disj.operator == '∨':
                            imp1 = conj.left
                            imp2 = conj.right
                            
                            # Verifica se a ordem do "e" bate perfeitamente com a ordem do "ou"
                            if disj.left == imp1.left and disj.right == imp2.left:
                                new_disjunction = Expression(operator='∨', left=imp1.right, right=imp2.right)
                                if new_disjunction not in memory:
                                    memory.append(new_disjunction)
                                    self.add_to_log(log, memory, [conj, disj], new_disjunction)
                                    print(f"Aplicando Dilema Construtivo: {conj}, {disj} ⇒ {new_disjunction}")
                                    return
                                    
                            # Verifica se a ordem do "e" está invertida em relação ao "ou"
                            # Ex: (n -> p) ^ (m -> p) com m v n
                            elif disj.left == imp2.left and disj.right == imp1.left:
                                new_disjunction = Expression(operator='∨', left=imp2.right, right=imp1.right)
                                if new_disjunction not in memory:
                                    memory.append(new_disjunction)
                                    self.add_to_log(log, memory, [conj, disj], new_disjunction)
                                    print(f"Aplicando Dilema Construtivo: {conj}, {disj} ⇒ {new_disjunction}")
                                    return

    def verify(self, memory, proposition):
        
        # 1. Verifica a forma de 3 premissas (referenciando as duas implicações e a disjunção separadas)
        for imp1 in memory:
            if hasattr(imp1, 'operator') and imp1.operator == '→':
                for imp2 in memory:
                    if hasattr(imp2, 'operator') and imp2.operator == '→' and imp1 != imp2:
                        for disj in memory:
                            if hasattr(disj, 'operator') and disj.operator == '∨' and \
                               (imp1.left == disj.left) and (imp2.left == disj.right):
                                
                                expected = Expression(operator='∨', left=imp1.right, right=imp2.right)
                                if proposition == expected:
                                    return True

        # 2. Verifica a forma de 2 premissas (referenciando a conjunção e a disjunção)
        for conj in memory:
            if hasattr(conj, 'operator') and conj.operator == '∧':
                if hasattr(conj.left, 'operator') and conj.left.operator == '→' and \
                   hasattr(conj.right, 'operator') and conj.right.operator == '→':
                    for disj in memory:
                        if hasattr(disj, 'operator') and disj.operator == '∨':
                            imp1 = conj.left
                            imp2 = conj.right
                            
                            # Combinação Direta
                            if disj.left == imp1.left and disj.right == imp2.left:
                                expected = Expression(operator='∨', left=imp1.right, right=imp2.right)
                                if proposition == expected:
                                    return True
                            
                            # Combinação Invertida
                            elif disj.left == imp2.left and disj.right == imp1.left:
                                expected = Expression(operator='∨', left=imp2.right, right=imp1.right)
                                if proposition == expected:
                                    return True
                                    
        return False
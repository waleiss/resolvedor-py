from ..interfaces import Observer
from ..expression import Expression

class Simplification(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, expr, simplified):
        log.append(
            f"({len(log) - 1}) {simplified}  Simplificação  "
            f"{memory.index(expr) + 1}"
        )

    def update(self, memory, log, conclusion=None):
        for expr in memory:
            if expr.operator == '∧':
                left = expr.left
                right = expr.right

                added = False
                if left not in memory:
                    memory.append(left)
                    self.add_to_log(log, memory, expr, left)
                    print(f"Aplicando Simplificação: {expr} ⇒ {left}")
                    added = True
                if right not in memory:
                    memory.append(right)
                    self.add_to_log(log, memory, expr, right)
                    print(f"Aplicando Simplificação: {expr} ⇒ {right}")
                    added = True
                
                if added:
                    return
    
    def verify(self, memory, proposition):
        for expr in memory:
            if expr.operator == '∧':
                left = expr.left
                right = expr.right
                
                if left == proposition or right == proposition:
                    return True
        
        return False
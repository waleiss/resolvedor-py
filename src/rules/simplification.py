from ..interfaces import Observer
from ..expression import Expression

class Simplification(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for expr in memory:
            if expr.operator == '∧':
                left = expr.left
                right = expr.right

                added = False
                if left not in memory:
                    memory.append(left)
                    print(f"Aplicando Simplificação: {expr} ⇒ {left}")
                    added = True
                if right not in memory:
                    memory.append(right)
                    print(f"Aplicando Simplificação: {expr} ⇒ {right}")
                    added = True
                
                if added:
                    return
    
    def verify(self, memory):
        for expr in memory:
            left = expr.left
            right = expr.right
            
            if left not in memory or right not in memory:
                return True
        
        return False
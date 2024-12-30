class Expression:
    def __init__(self, operator=None, left=None, right=None):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self, top_level=True):
        if self.operator is None:
            # Átomo simples
            return str(self.left)
        
        if self.operator == '¬':
            # Negação
            return f"¬{self.left.__str__(top_level=False)}"
        
        # Expressões binárias
        left_str = self.left.__str__(top_level=False)
        right_str = self.right.__str__(top_level=False)
        
        # Adiciona parênteses apenas se não for top-level
        expr_str = f"{left_str} {self.operator} {right_str}"
        if top_level:
            return expr_str
        return f"({expr_str})"
    
    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        # Verifica se duas expressões são iguais
        if isinstance(other, Expression):
            return (
                self.operator == other.operator and
                self.left == other.left and
                self.right == other.right
            )
        return False
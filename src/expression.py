class Expression:
    def __init__(self, operator=None, left=None, right=None):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        if self.operator == '→':
            return f"({self.left} {self.operator} {self.right})"
        if self.operator == '¬':
            return f"({self.operator}{self.left})"
        return str(self.left)  # Nó folha ou expressão atômica

    def __eq__(self, other):
        # Verifica se duas expressões são iguais
        if isinstance(other, Expression):
            return (
                self.operator == other.operator and
                self.left == other.left and
                self.right == other.right
            )
        return False
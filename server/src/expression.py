from typing import Optional, Union


class Expression:
    def __init__(self, left: Union[str, "Expression"], operator: Optional[str] = None, right: Optional[Union[str, "Expression"]] = None):
        self.operator: Optional[str] = operator
        self.left: Union[str, "Expression"] = left
        self.right: Optional[Union[str, "Expression"]] = right

    def _format_operand(self, operand: Union[str, "Expression", None]) -> str:
        """Helper method to format an operand, adding parentheses if needed."""
        if isinstance(operand, Expression):
            return operand._to_string(top_level=False)
        return str(operand)

    def _to_string(self, top_level: bool = True) -> str:
        if self.operator is None:
            # Átomo simples
            return str(self.left)
        
        if self.operator == '¬':
            # Negação
            return f"¬{self._format_operand(self.left)}"
        
        # Expressões binárias
        left_str = self._format_operand(self.left)
        right_str = self._format_operand(self.right)
        
        # Adiciona parênteses apenas se não for top-level
        expr_str = f"{left_str} {self.operator} {right_str}"
        if top_level:
            return expr_str
        return f"({expr_str})"

    def __str__(self):
        return self._to_string(top_level=True)
    
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
from .expression import Expression

def parse_expression(input_str):
    """Converte uma string para um objeto Expression."""
    input_str = input_str.strip()

    if not is_balanced(input_str):
        raise ValueError("Parênteses desbalanceados na expressão!")

    # Identifica operadores principais fora de parênteses
    depth = 0
    for i, char in enumerate(input_str):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char in {'→', '↔', '∧', '∨'} and depth == 0:  # Operadores binários
            p_left = input_str[:i].strip()
            p_right = input_str[i + 1:].strip()

            #Retira o parenteses antes de chamar a recursão, para que consiga identificar o operador principal da subexpressão
            #Exemplo: (P -> Q) -> R, ele consegue achar o segundo implica pois nao tem parenteses, mas na hora de olhar o (P -> Q) o depth nao vai ser 0
            if p_left.startswith('(') and p_left.endswith(')'):
                p_left = p_left[1:-1]
            if p_right.startswith('(') and p_right.endswith(')'):
                p_right = p_right[1:-1]
            
            left = parse_expression(p_left)
            right = parse_expression(p_right)
            return Expression(operator=char, left=left, right=right)
    
        # Verifica negação (¬)
    if input_str.startswith('¬'):
        p_inner = input_str[1:].strip()
        if p_inner.startswith('(') and p_inner.endswith(')'):
                p_inner = p_inner[1:-1]
        inner_expr = parse_expression(p_inner)
        return Expression(operator='¬', left=inner_expr)
    

    # Se não há operadores, é um átomo simples
    return Expression(left=input_str)

def is_balanced(input_str):
    """Verifica se os parênteses de uma expressão estão balanceados."""
    depth = 0
    for char in input_str:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0

#O PROGRAMA PRECISA EXATAMENTE DA ENTRADA SEM PARENTESES NO LADO MAIS FORA POSSIVEL, PARA QUE ELE CONSIGA IDENTIFICAR O OPERADOR PRINCIPAL
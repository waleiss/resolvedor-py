from src import *

def parse_expression(input_str):
    """Converte uma string para um objeto Expression."""
    input_str = input_str.strip()

    # Verifica negação (¬)
    if input_str.startswith('¬'):
        inner_expr = parse_expression(input_str[1:])
        return Expression(operator='¬', left=inner_expr)

    # Verifica parênteses para expressões compostas
    if input_str.startswith('(') and input_str.endswith(')'):
        input_str = input_str[1:-1]

    # Identifica operadores principais fora de parênteses
    depth = 0
    for i, char in enumerate(input_str):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char in {'∨', '→'} and depth == 0:  # Operadores binários
            left = parse_expression(input_str[:i])
            right = parse_expression(input_str[i + 1:])
            return Expression(operator=char, left=left, right=right)

    # Se não há operadores, é um átomo simples
    return Expression(left=input_str)

def main():
    memory = []  # Lista inicial de memória

    print("Bem-vindo ao sistema de lógica proposicional!")
    print("Digite expressões no formato: '¬A', '(A ∨ B)', '(A → B)'")
    print("Digite 'sair' para encerrar.")
    
    while True:
        user_input = input("Digite uma expressão: ").strip()
        if user_input.lower() == 'sair':
            break
        
        try:
            expr = parse_expression(user_input)  # Converte string para Expression
            memory.append(expr)  # Adiciona à memória
            print(f"Memória atual: {memory}")
        except Exception as e:
            print(f"Erro ao processar a expressão: {e}")

if __name__ == "__main__":
    main()

import re
from .rules import *  # Importa todas as regras
from .expression import Expression
from .parser import parse_expression

def extract_references(step):
        """
        Extrai os índices referenciados de um passo do log.
        Exemplo de entrada: "(13) (P ∨ S)  Adição  9, 6"
        Retorna: [9, 6]
        """
        import re
        match = re.findall(r'\b\d+\b', step)
        return [int(num) for num in match]  # Ignorar o número do próprio passo

def process_inferences(inferences, rules_dict, memory, log):
    """
    Processa as inferências recebidas, extrai a regra usada e as premissas referenciadas.
    """
    for inference in inferences:
        # Divide usando dois espaços como delimitador
        parts = inference.split("  ")
        if len(parts) == 4:
            step_info, expression_str, rule_name, refs = parts
            
            # Extrair número do passo e a expressão
            step_number = int(re.match(r"\((\d+)\)", step_info).group(1))  # Número do passo
            new_expr = parse_expression(expression_str)  # Parse da expressão
            
            # Adicionar a expressão à memória
            memory.append(new_expr)
            
            # Extrair a regra e as referências
            references = extract_references(refs)  # Avaliar a lista de referências
            
            # Verificar se a regra está no dicionário
            if rule_name in rules_dict:
                rule = rules_dict[rule_name]
                # Criar lista com as expressões referenciadas
                referenced_expressions = [memory[i-1] for i in references]  # Referências são 1-based
                
                # Chamar o método verify() da regra
                if rule.verify(referenced_expressions, new_expr):
                    log.append(f"Inferência válida: {inference}")
                else:
                    log.append(f"Inferência inválida: {inference}")
            else:
                print(f"Regra não encontrada: {rule_name}")
        else:
            print(f"Formato inválido de inferência: {inference}")
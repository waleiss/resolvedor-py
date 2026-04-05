import re
from .rules import *
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

def process_inferences(inferences, rules_dict, memory, log, conclusion):
    """
    Processa as inferências recebidas, extrai a regra usada e as premissas referenciadas.
    Rastreia passos inválidos e invalida todos os passos que dependem deles.
    Avalia se a conclusão final foi alcançada com sucesso.
    """
    # Inicializar valid_steps com os índices das premissas já na memória
    valid_steps = set(range(1, len(memory) + 1))  # Premissas são passos válidos por padrão
    
    # Flag para saber se a conclusão foi gerada em algum passo válido
    conclusion_reached = False
    
    for inference in inferences:
        # Divide usando dois espaços como delimitador
        parts = inference.split(' | ')
        if len(parts) == 4:
            step_info, expression_str, rule_name, refs = parts
            
            # Extrair número do passo e a expressão
            step_number = int(re.match(r"\((\d+)\)", step_info).group(1))  # Número do passo
            new_expr = parse_expression(expression_str)  # Parse da expressão
            
            # Adicionar a expressão à memória
            memory.append(new_expr)
            
            # Extrair a regra e as referências
            references = extract_references(refs)  # Avaliar a lista de referências
            
            # Verificar se alguma referência é de um passo inválido
            depends_on_invalid = any(ref not in valid_steps for ref in references if ref > 0)
            
            if depends_on_invalid:
                log.append(f"Inferência inválida (depende de passo inválido): {inference}")
                continue
            
            # Verificar se a regra está no dicionário
            if rule_name in rules_dict:
                rule = rules_dict[rule_name]
                # Criar lista com as expressões referenciadas
                referenced_expressions = [memory[i-1] for i in references if i > 0]  # Referências são 1-based
                
                # Chamar o método verify() da regra
                if rule.verify(referenced_expressions, new_expr):
                    valid_steps.add(step_number)  # Marcar como válido
                    log.append(f"Inferência válida: {inference}")
                    
                    # Checa se o passo atual atingiu a conclusão do problema
                    if new_expr == conclusion:
                        conclusion_reached = True
                else:
                    log.append(f"Inferência inválida: {inference}")
            else:
                log.append(f"Inferência inválida (regra não encontrada: {rule_name}): {inference}")
        else:
            print(f"Formato inválido de inferência: {inference}")

    # Adiciona o veredito final ao log
    if conclusion_reached:
        log.append("Conclusão alcançada com sucesso.")
    else:
        log.append("Conclusão não alcançada.")
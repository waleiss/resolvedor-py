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
        match = re.findall(r'\b\d+\b', step)
        return [int(num) for num in match]  # Ignorar o número do próprio passo

def process_inferences(inferences, rules_dict, memory, log, llm_feedback_generator=None):
    """
    Processa as inferências recebidas, extrai a regra usada e as premissas referenciadas.
    """
    
    results = {
        "valid_inferences": [],
        "invalid_inferences": [],
        "total_inferences": len(inferences),
        "success_rate": 0.0
    }
    
    for inference in inferences:
        parts = inference.split("  ")
        if len(parts) == 3:
            expression_str, rule_name, refs = parts
            
            try:
                # Extract expression
                new_expr = parse_expression(expression_str)
                
                # Add expression to memory
                memory.append(new_expr)
                
                # Extract rule and references
                references = extract_references(refs)
                
                # Verify if rule exists
                if rule_name in rules_dict:
                    rule = rules_dict[rule_name]
                    referenced_expressions = [memory[i-1] for i in references]
                    
                    # Verify the rule application
                    if rule.verify(referenced_expressions, new_expr):
                        log.append(f"Inferência válida: {inference}")
                        results["valid_inferences"].append(inference)
                    else:
                        log.append(f"Inferência inválida: {inference}")
                        results["invalid_inferences"].append(inference)
                else:
                    log.append(f"Regra não encontrada: {rule_name} em {inference}")
                    results["invalid_inferences"].append(inference)
                    
            except Exception as e:
                log.append(f"Erro ao processar inferência: {inference} - {str(e)}")
                results["invalid_inferences"].append(inference)
        else:
            log.append(f"Formato inválido de inferência: {inference}")
            results["invalid_inferences"].append(inference)
    
    # Calculate success rate
    if results["total_inferences"] > 0:
        results["success_rate"] = len(results["valid_inferences"]) / results["total_inferences"]
    
    return results
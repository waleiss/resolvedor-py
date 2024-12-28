def filter_relevant_steps(log, conclusion_index):
        """
        Filtra do log de execução os passos relevantes que levaram à solução.
        """
        # Identifica o índice da linha de separação
        separator_index = next((i for i, step in enumerate(log) if '----' in step), None)
        
        if separator_index is None:
            raise ValueError("Linha de separação não encontrada no log.")
        
        # Adiciona todos os passos acima da linha de separação
        relevant_steps = set(range(separator_index + 1))
        
        # Pilha para realizar a busca
        stack = [conclusion_index]

        while stack:
            current_index = stack.pop()
            # Evita processar passos já adicionados
            if current_index in relevant_steps:
                continue
            # Adiciona o passo atual ao conjunto de relevantes
            relevant_steps.add(current_index)
            # Recupera o passo atual no log
            step = log[current_index]
            # Extrai os índices referenciados na justificativa (números após "Adição", "Silogismo", etc.)
            references = extract_references(step)
            
            # Adiciona os passos referenciados à pilha
            for ref in references:
                if ref - 1 >= 0 and ref - 1 < len(log):  # Garantir que o índice é válido
                    stack.append(ref + 1)  # Ajuste do índice para 0-base
        
        # Ordena os passos relevantes
        return sorted(relevant_steps)

def extract_references(step):
        """
        Extrai os índices referenciados de um passo do log.
        Exemplo de entrada: "(13) (P ∨ S)  Adição  9, 6"
        Retorna: [9, 6]
        """
        import re
        match = re.findall(r'\b\d+\b', step)
        return [int(num) for num in match[1:]]  # Ignorar o número do próprio passo
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import List

load_dotenv()

class GeminiService:
    """Serviço para interação com a API do Gemini"""
    
    def __init__(self):
        """Inicializa o cliente do Gemini com a API key do .env"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3-flash-preview"
    
    def solve_problem(self, problem: str, sentences: List[str], conclusion: str) -> dict:
        """
        Pede ao Gemini para resolver um problema de lógica proposicional.
        
        Args:
            problem: String com o problema formatado (sentenças ⊢ conclusão)
            sentences: Lista de sentenças (premissas)
            conclusion: Conclusão a ser provada
            
        Returns:
            dict com a solução do Gemini e inferências extraídas
        """
        prompt = self._build_solver_prompt(problem, sentences, conclusion)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            # Extrai as inferências da resposta do Gemini
            solution_text = response.text
            inferences = self._extract_inferences(solution_text)
            
            return {
                "success": True,
                "solution": solution_text,
                "inferences": inferences,
                "model": self.model_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model_id
            }
    
    def _build_solver_prompt(self, problem: str, sentences: List[str], conclusion: str) -> str:
        """Constrói o prompt para o Gemini resolver o problema"""
        sentences_formatted = "\n".join([f"{i+1}. {s}" for i, s in enumerate(sentences)])
        
        prompt = f"""Você é um especialista em lógica proposicional. Resolva o seguinte problema usando regras de inferência ou equivalência válidas.

    **Problema:**
    {problem}

    **Premissas:**
    {sentences_formatted}

    **Conclusão a provar:**
    {conclusion}

    **Instruções:**
    1. Use apenas regras de inferência ou equivalência válidas (Silogismo Disjuntivo, Modus Tollens, Introdução da Bi-implicação, Dissociação de Bi-implicação, Modus Ponens, Silogismo Hipotético, Transposição, Associatividade, Comutatividade, Distributividade, De Morgan, Dilema Construtivo, Exportação, Implicação Material, Conjunção, Simplificação, Dupla Negação e Adição).
    2. Simplifique diretamente novas expressões que contenham dupla negação (ex: ao inferir ¬(¬P) ∨ Q, elimine a negação e escreva P ∨ Q em vez de ¬(¬P) ∨ Q).
    3. Para cada passo da dedução, forneça EXATAMENTE no formato:
       (N) expressão | Nome_da_Regra | premissas_usadas
       
       Onde tem esses 4 campos separados por " | " os quais:
       - N é o número sequencial do passo (começando após as premissas iniciais)
       - expressão é a nova fórmula derivada
       - Nome_da_Regra é o nome exato da regra aplicada (ex: "Modus Ponens", "Adição", "Simplificação")
       - premissas_usadas são os números das linhas usadas, separados por vírgula

    **Exemplos de formato esperado:**
    ({len(sentences)+1}) P | Simplificação | 1
    ({len(sentences)+2}) P → Q | Dissociação de Bi-implicação | {len(sentences)+2}
    ({len(sentences)+3}) Q | Modus Ponens | {len(sentences)+1}, {len(sentences)+2}

    Forneça a solução completa passo a passo."""

        return prompt
    
    def _extract_inferences(self, solution_text: str) -> List[str]:
        """
        Extrai as inferências formatadas da resposta do Gemini.
        Procura por linhas no formato: (N) expressão | Regra | refs
        """
        import re
        
        inferences = []
        # Regex para capturar linhas no formato esperado
        pattern = r'\((\d+)\)\s+(.+?)\s+\|\s+(.+?)\s+\|\s+(.+?)(?:\n|$)'
        
        matches = re.findall(pattern, solution_text, re.MULTILINE)
        
        for match in matches:
            step_num, expression, rule, refs = match
            # Reconstrói no formato esperado pelo avaliador
            inference = f"({step_num}) | {expression.strip()} | {rule.strip()} | {refs.strip()}"
            inferences.append(inference)
        
        return inferences
    
    def evaluate_solution(self, problem: str, solution_log: List[str]) -> dict:
        """
        Envia a solução do problema para o Gemini avaliar.
        
        Args:
            problem: String com o problema original (sentenças ⊢ conclusão)
            solution_log: Lista de strings com o log de resolução
            
        Returns:
            dict com a avaliação do Gemini
        """
        # Monta o prompt para o Gemini
        prompt = self._build_evaluation_prompt(problem, solution_log)
        
        try:
            # Chama a API do Gemini
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            return {
                "success": True,
                "evaluation": response.text,
                "model": self.model_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model_id
            }
    
    def _build_evaluation_prompt(self, problem: str, solution_log: List[str]) -> str:
        """Constrói o prompt para avaliação do Gemini"""
        log_text = "\n".join(solution_log)
        
        prompt = f"""Você é um especialista em lógica proposicional. Analise a resolução do problema abaixo e avalie, para cada dos passos da solução (ou seja, não considerar as premissas acima da linha '------------'), o seguinte:

1. Se a resolução está correta e se as regras de inferência foram aplicadas adequadamente.
2. Se há algum erro ou inconsistência, explique o que está errado na solução.

**Problema:**
{problem}

**Resolução apresentada:**
{log_text}

Por favor, forneça uma avaliação sucinta e objetiva. Além disso, analise a qualidade da solução (por exemplo, se ela poderia ser otimizada)."""

        return prompt
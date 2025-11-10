import os
from google import genai
from google.genai import types
from typing import List


class GeminiService:
    """Serviço para interação com a API do Gemini"""
    
    def __init__(self):
        """Inicializa o cliente do Gemini com a API key do .env"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"
    
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

1. Se a resolução está correta e se as regras de inferência foram aplicadas adequadamente
2. Se há algum erro ou inconsistência, explique o que está errado na solução

**Problema:**
{problem}

**Resolução apresentada:**
{log_text}

Por favor, forneça uma avaliação sucinta e objetiva."""

        return prompt
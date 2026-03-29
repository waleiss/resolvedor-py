import os
from dotenv import load_dotenv
from google import genai
from typing import List
from pydantic import BaseModel, Field

load_dotenv()


class LogicalStep(BaseModel):
    """Representa um passo lógico na dedução"""
    step_n: int = Field(description="Número sequencial do passo")
    expression_str: str = Field(description="Expressão lógica derivada")
    rule_name: str = Field(description="Nome da regra aplicada")
    refs: list[int] = Field(description="Referências das linhas utilizadas")


class LogicalSolution(BaseModel):
    """Resposta estruturada do solver"""
    passos: List[LogicalStep]


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
        Retorna sempre um JSON estruturado com os passos da dedução.
        
        Args:
            problem: String com o problema formatado (sentenças ⊢ conclusão)
            sentences: Lista de sentenças (premissas)
            conclusion: Conclusão a ser provada
            
        Returns:
            dict com a solução do Gemini e inferências extraídas em formato JSON
        """
        prompt = self._build_solver_prompt(problem, sentences, conclusion)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": LogicalSolution.model_json_schema()
                }
            )
            
            # Valida o JSON retornado pelo modelo contra o schema Pydantic
            parsed_solution = LogicalSolution.model_validate_json(response.text)
            passos = [passo.model_dump() for passo in parsed_solution.passos]
            
            # Converte para formato esperado pelo process_solution
            inferences = self._convert_steps_to_inferences(parsed_solution.passos)
            
            return {
                "success": True,
                "inferences": inferences,
                "model": self.model_id,
                "passos": passos   #por enquanto nao tem uso
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model_id
            }
    
    def _build_solver_prompt(self, problem: str, sentences: List[str], conclusion: str) -> str:
        """Constrói o prompt para o Gemini resolver o problema com saída JSON estruturada"""
        sentences_formatted = "\n".join([f"{i+1}. {s}" for i, s in enumerate(sentences)])
        
        prompt = f"""Resolva o problema de lógica proposicional abaixo com passos formais válidos.

Retorne APENAS JSON no formato:
{{
  "passos": [
    {{
      "step_n": <int>,
      "expression_str": "<expressão>",
      "rule_name": "<regra>",
      "refs": [<int>, ...]
    }}
  ]
}}

Regras permitidas:
Silogismo Disjuntivo, Modus Tollens, Introdução da Bi-implicação, Dissociação de Bi-implicação, Modus Ponens, Silogismo Hipotético, Transposição, Associatividade, Comutatividade, Distributividade, De Morgan, Dilema Construtivo, Exportação, Implicação Material, Conjunção, Simplificação, Dupla Negação e Adição.

Restrições:
- Simplifique diretamente novas expressões que contenham dupla negação (ex: ao inferir ¬¬P ∨ Q, elimine a negação e escreva P ∨ Q em vez de ¬¬P ∨ Q.
- Sem texto fora do JSON.
- Sem LaTeX e sem blocos de código.
- Use apenas símbolos lógicos Unicode: ¬, →, ↔, ∧, ∨.
- step_n começa em {len(sentences) + 1}.
- refs deve conter as linhas usadas em cada inferência.
- A lista deve ir até derivar a conclusão {conclusion}.

Problema: {problem}
Premissas:
{sentences_formatted}
Conclusão: {conclusion}
"""

        return prompt
    
    def _convert_steps_to_inferences(self, passos: List[LogicalStep]) -> List[str]:
        """
        Converte passos JSON estruturados para o formato esperado pelo process_solution.
        Formato de saída: "(N) | expression_str | rule_name | ref1, ref2, ..."
        """
        inferences = []
        for passo in passos:
            step_n = passo.step_n
            expression_str = passo.expression_str.strip()
            rule_name = passo.rule_name.strip()
            refs = passo.refs
            refs_str = ", ".join(str(p) for p in refs)
            
            inference = f"({step_n}) | {expression_str} | {rule_name} | {refs_str}"
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
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import Any, Dict, List, Literal, Optional
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


class EvaluationStepReview(BaseModel):
    """Revisão estruturada de um passo da solução"""
    step_n: int = Field(description="Número do passo avaliado")
    status: Literal["válido", "inválido"] = Field(description="Status do passo")
    rule_name: str = Field(description="Nome da regra citada")
    refs: list[int] = Field(description="Referências usadas no passo")
    explanation: str = Field(description="Explicação curta do julgamento")


class StructuredEvaluation(BaseModel):
    """Saída estruturada da avaliação do Gemini"""
    summary: str
    step_reviews: List[EvaluationStepReview]
    optimization_notes: List[str] = Field(default_factory=list)


class AnalysisOutput(BaseModel):
    """Análise estruturada da qualidade/correção da solução"""
    num_steps: int = Field(ge=0)
    num_valid_steps: int = Field(ge=0)
    num_invalid_steps: int = Field(ge=0)
    reaches_target_conclusion: bool
    is_fully_correct: bool
    error_type: Optional[
        Literal[
            "aplicação inválida de regra",
            "regra inexistente",
            "conclusão não alcançada",
            "uso incorreto de referência a linhas anteriores",
        ]
    ] = None


class GeminiService:
    """Serviço para interação com a API do Gemini"""
    
    def __init__(self):
        """Inicializa o cliente do Gemini com a API key do .env"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3-flash-preview"
        self.analysis_model_id = "gemini-3.1-flash-lite-preview"
    
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
                    "response_json_schema": LogicalSolution.model_json_schema(),
                    "thinking_config": types.ThinkingConfig(thinking_level="high"),
                    "temperature": 1.0,
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
        
        prompt = f"""Você é um especialista em Lógica Proposicional. Resolva o problema de lógica proposicional abaixo fornecendo uma construção de prova passo a passo com passos formais válidos usando dedução natural.

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

Restrições obrigatórias:
- Use somente as regras permitidas e escreva o nome da regra EXATAMENTE como listado.
- Cada passo deve ser derivado apenas das premissas ou de linhas anteriores válidas.
- Não pule etapas necessárias.
- Não gere passos redundantes que não contribuam para alcançar a conclusão.
- step_n deve ser estritamente crescente, sem repetições, iniciando em {len(sentences)+1}.
- refs deve conter somente números de linhas anteriores efetivamente usados.
- A prova deve terminar quando a conclusão {conclusion} for derivada.
- Use apenas símbolos Unicode: ¬, →, ↔, ∧, ∨.
- Não use LaTeX, Markdown ou texto fora do JSON.
- Simplifique diretamente novas expressões que contenham dupla negação (ex: ao inferir ¬¬P ∨ Q, elimine a negação e escreva P ∨ Q em vez de ¬¬P ∨ Q.

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
        prompt = self._build_evaluation_prompt(problem, solution_log)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": StructuredEvaluation.model_json_schema(),
                    "thinking_config": types.ThinkingConfig(thinking_level="high"),
                    "temperature": 1.0,
                    }
            )
            
            parsed = StructuredEvaluation.model_validate_json(response.text)
            return {
                "success": True,
                "evaluation": parsed.model_dump(),
                "log": self._structured_evaluation_to_log(parsed),
                "model": self.model_id,
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
        
        prompt = f"""Você é um especialista em lógica proposicional.

    Analise a resolução do problema abaixo passo a passo e retorne APENAS JSON com:
    - summary
    - step_reviews
    - optimization_notes

    Critérios de avaliação:
    - identifique se cada passo é válido ou inválido e se as regras de inferência e equivalência foram aplicadas corretamente;
    - registre a regra usada e as referências;
    - se houver erro, explique o erro na explicação do julgamento;
    - aponte se a conclusão foi alcançada corretamente;
    - indique se a solução está totalmente correta;
    - nas notas de otimização, descreva como a solução poderia ser otimizada;
    - a explicação deve ser adaptada para alunos de graduação em cursos introdutórios de lógica, ou seja, você deve definir quaisquer termos técnicos e explicar cada etapa claramente;
    - regras de inferência e equivalência permitidas: Silogismo Disjuntivo, Modus Tollens, Introdução da Bi-implicação, Dissociação de Bi-implicação, Modus Ponens, Silogismo Hipotético, Transposição, Associatividade, Comutatividade, Distributividade, De Morgan, Dilema Construtivo, Exportação, Implicação Material, Conjunção, Simplificação, Dupla Negação e Adição.

    Problema:
    {problem}

    Resolução apresentada:
    {log_text}
    """

        return prompt

    def _structured_evaluation_to_log(self, evaluation: StructuredEvaluation) -> List[str]:
        log = [
            "===== RESUMO =====",
            evaluation.summary,
            "",
            "===== AVALIAÇÃO PASSO A PASSO =====",
        ]

        for review in evaluation.step_reviews:
            refs_text = ", ".join(str(ref) for ref in review.refs) if review.refs else "nenhuma"
            
            status_icon = "✓" if review.status == "válido" else "✗"
            status_text = "VÁLIDO" if review.status == "válido" else "INVÁLIDO"

            log.extend([
                f"{status_icon} Passo {review.step_n} ({status_text})",
                f"  Regra: {review.rule_name}",
                f"  Referências: {refs_text}",
                f"  Justificativa: {review.explanation}",
                ""
            ])

        if evaluation.optimization_notes:
            log.extend([
                "===== OTIMIZAÇÕES ====="
            ])
            for note in evaluation.optimization_notes:
                log.append(f"- {note}")

        return log

    def generate_structured_analysis(
        self,
        pipeline: str,
        problem_data: Dict[str, Any],
        solver_output: Dict[str, Any],
        evaluation_output: Dict[str, Any],
    ) -> dict:
        """
        Gera o campo analysis estruturado para ambos os pipelines.
        Usa gemini-3.1-flash-lite-preview com schema estrito.
        """
        prompt = self._build_analysis_prompt(pipeline, problem_data, solver_output, evaluation_output)

        try:
            response = self.client.models.generate_content(
                model=self.analysis_model_id,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": AnalysisOutput.model_json_schema(),
                    "thinking_config": types.ThinkingConfig(thinking_level="high"),
                    "temperature": 1.0,
                },
            )

            parsed = AnalysisOutput.model_validate_json(response.text)
            return {
                "success": True,
                "analysis": parsed.model_dump(),
                "model": self.analysis_model_id,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.analysis_model_id,
            }

    def _build_analysis_prompt(
        self,
        pipeline: str,
        problem_data: Dict[str, Any],
        solver_output: Dict[str, Any],
        evaluation_output: Dict[str, Any],
    ) -> str:
        """Monta prompt para análise estruturada com saída JSON estrita."""
        return f"""Você deve analisar uma prova de lógica proposicional e retornar APENAS JSON válido no schema fornecido.

Critérios:
- num_steps: quantidade total de passos da solução (solver_output.steps_raw).
- num_valid_steps: quantidade de passos válidos identificados.
- num_invalid_steps: quantidade de passos inválidos identificados.
- reaches_target_conclusion: true se a conclusão-alvo foi alcançada.
- is_fully_correct: true somente se todos os passos forem válidos E a conclusão for alcançada.
- error_type: null quando não houver erro; caso contrário use EXATAMENTE um dos valores:
  1) aplicação inválida de regra
  2) regra inexistente
  3) conclusão não alcançada
  4) uso incorreto de referência a linhas anteriores

Regras de interpretação:
- Se houver log do avaliador com "Inferência inválida (regra não encontrada", use "regra inexistente".
- Se houver log com referências inconsistentes, use "uso incorreto de referência a linhas anteriores".
- Se houver "Inferência inválida" por aplicação da regra ou "depende de passo inválido", use "aplicação inválida de regra".
- Se não alcançar a conclusão solicitada, use "conclusão não alcançada".

Dados de entrada:
pipeline: {pipeline}
problem_data: {problem_data}
solver_output: {solver_output}
evaluation_output: {evaluation_output}
"""
    
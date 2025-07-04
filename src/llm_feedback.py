import google.generativeai as genai
from typing import List, Dict, Any

class LLMFeedbackGenerator:
    def __init__(self, api_key: str):
        """
        Initialize the LLM feedback generator with Gemini API.
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_feedback(self, premises: List[str], conclusion: str, 
                         inferences: List[str], evaluation_log: List[str]) -> Dict[str, Any]:
        """
        Generate educational feedback based on evaluation results.
        
        Args:
            premises: List of premise strings
            conclusion: Conclusion string
            inferences: List of inference strings
            evaluation_log: Log from the evaluator
            
        Returns:
            Dictionary with feedback information
        """
        # Analyze the evaluation log to identify errors
        errors = self._extract_errors(evaluation_log)
        
        if not errors:
            return {
                "status": "success",
                "message": "Todas as inferências estão corretas! Parabéns!",
                "feedback": None
            }
        
        # Generate feedback for errors
        feedback = self._generate_error_feedback(premises, conclusion, inferences, errors)
        
        return {
            "status": "error",
            "message": f"Encontrados {len(errors)} erro(s) nas inferências.",
            "errors": errors,
            "feedback": feedback
        }
    
    def _extract_errors(self, evaluation_log: List[str]) -> List[Dict[str, str]]:
        """Extract error information from evaluation log."""
        errors = []
        for log_entry in evaluation_log:
            if "Inferência inválida:" in log_entry:
                # Extract the invalid inference
                invalid_inference = log_entry.replace("Inferência inválida: ", "")
                errors.append({
                    "inference": invalid_inference,
                    "type": "invalid_inference"
                })
        return errors
    
    def _generate_error_feedback(self, premises: List[str], conclusion: str, 
                                inferences: List[str], errors: List[Dict]) -> str:
        """Generate educational feedback using Gemini."""
        
        # Prepare the prompt for Gemini
        prompt = self._create_feedback_prompt(premises, conclusion, inferences, errors)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao gerar feedback: {str(e)}"
    
    def _create_feedback_prompt(self, premises: List[str], conclusion: str, 
                               inferences: List[str], errors: List[Dict]) -> str:
        """Create a detailed prompt for Gemini to generate educational feedback."""
        
        prompt = f"""
                    O estudante tentou resolver um problema de inferência lógica, mas cometeu erros.

                    PROBLEMA:
                    Premissas: {', '.join(premises)}
                    Conclusão: {conclusion}

                    TENTATIVA DO ESTUDANTE:
                    {chr(10).join(inferences)}

                    ERROS IDENTIFICADOS:
                    {chr(10).join([f"- {error['inference']}" for error in errors])}

                    Por favor, forneça um feedback breve e direto, seguindo este formato:

                    1. ERRO PRINCIPAL:
                    - Nome da regra usada de forma incorreta
                    - Por que a aplicação está errada (1 ou 2 frases)

                    2. CONCEITO A REVISAR:
                    - Nome do conceito
                    - Explicação rápida (1 ou 2 frases)

                    3. COMO CORRIGIR:
                    - Qual regra deveria ter sido usada
                    - Como aplicar corretamente (exemplo rápido)

                    Mantenha o feedback curto (máximo de 3 parágrafos pequenos) e focado no principal erro.

                    Regras de inferência disponíveis:
                    - Modus Ponens, Modus Tollens
                    - Silogismo Disjuntivo, Silogismo Hipotético
                    - Adição, Simplificação, Conjunção
                    - De Morgan, Dupla Negação
                    - Transposição, Implicação Material
                    - Associatividade, Comutatividade, Distributividade
                    - Dilema Construtivo, Exportação
                    - Introdução/Dissociação da Bi-implicação

                    Seja específico, didático e encorajador. O objetivo é ajudar o estudante a aprender com os erros.
        """
        return prompt
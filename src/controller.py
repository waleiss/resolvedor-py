import time
from .filter_steps import filter_relevant_steps
from .process_solution import process_inferences
from .llm_feedback import LLMFeedbackGenerator
class Controller:
    def __init__(self, rules, memory, conclusion, log, gemini_api_key="None"):
        self.rules = rules  # Lista de regras (agentes)
        self.memory = memory  # Memória de trabalho compartilhada
        self.conclusion = conclusion  # Conclusão a ser provada
        self.log = log  # Log de execução
        self.llm_feedback = None

        if gemini_api_key:
            try:
                self.llm_feedback = LLMFeedbackGenerator(gemini_api_key)
            except Exception as e:
                print(f"Erro ao inicializar LLM feedback: {e}")


    def run_solver(self):
        """Executa todas as regras de forma sequencial."""
        print('')
        time_limit = 10
        start_time = time.time()

        while self.conclusion not in self.memory:
            # Verifica se o limite de tempo foi excedido
            if time.time() - start_time > time_limit:
                self.log.append("Tempo limite excedido. A conclusão não foi alcançada.")
                break
            # Tenta aplicar a regra
            for rule in self.rules:
                if self.conclusion not in self.memory:
                    rule.update(self.memory, self.log, self.conclusion)

        print('')
        # Exibe o log de execução
        for step in self.log:
            print(step)
        print('')

        print('Passos realmente relevantes:')
        # Exibe o log de execução
        passos = filter_relevant_steps(self.log, len(self.log) - 1)

        for step in self.log:
            if self.log.index(step) in passos:
                print(step)
        print('')

    
    def run_evaluator(self, inferences, premises_str=None, conclusion_str=None):
        """
        Run evaluator with optional LLM feedback.
        
        Args:
            inferences: List of inference strings
            premises_str: List of premise strings for feedback
            conclusion_str: Conclusion string for feedback
        """
        # Process inferences
        results = process_inferences(
            inferences, self.rules, self.memory, self.log, self.llm_feedback
        )
        
        # Print evaluation results
        print('\n--- RESULTADO DA AVALIAÇÃO ---')
        for step in self.log:
            print(step)
        
        print(f'\n--- ESTATÍSTICAS ---')
        print(f'Total de inferências: {results["total_inferences"]}')
        print(f'Inferências válidas: {len(results["valid_inferences"])}')
        print(f'Inferências inválidas: {len(results["invalid_inferences"])}')
        print(f'Taxa de sucesso: {results["success_rate"]:.2%}')
        
        # Generate LLM feedback if there are errors and LLM is available
        if results["invalid_inferences"] and self.llm_feedback and premises_str and conclusion_str:
            print('\n--- FEEDBACK EDUCATIVO ---')
            try:
                feedback_result = self.llm_feedback.generate_feedback(
                    premises_str, conclusion_str, inferences, self.log
                )
                
                if feedback_result["status"] == "error":
                    print(feedback_result["message"])
                    print('\n' + feedback_result["feedback"])
                else:
                    print(feedback_result["message"])
                    
            except Exception as e:
                print(f'Erro ao gerar feedback: {e}')
        
        return results
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class StorageService:
    """Serviço para armazenar resultados em arquivos JSON"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa o serviço de armazenamento.
        
        Args:
            data_dir: Diretório onde os arquivos serão salvos
        """
        self.data_dir = Path(data_dir)
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_experiment_result(
        self,
        problem: str,
        sentences: List[str],
        conclusion: str,
        solver_log: List[str],
        gemini_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Salva o resultado de um experimento em arquivo JSON.
        
        Args:
            problem: Descrição do problema
            sentences: Lista de sentenças (premissas)
            conclusion: Conclusão do problema
            solver_log: Log de resolução do solver
            gemini_evaluation: Avaliação do Gemini
            
        Returns:
            Dict com informações sobre o arquivo salvo
        """
        # Gera timestamp e nome do arquivo
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"experiment_{timestamp_str}.json"
        filepath = self.data_dir / filename
        
        # Monta o objeto de resultado
        result = {
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "filename": filename
            },
            "problem": {
                "description": problem,
                "sentences": sentences,
                "conclusion": conclusion
            },
            "solver_result": {
                "log": solver_log
            },
            "gemini_evaluation": gemini_evaluation
        }
        
        # Salva o arquivo
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "filepath": str(filepath),
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_experiments(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de todos os experimentos salvos.
        
        Returns:
            Lista de dicionários com informações dos experimentos
        """
        experiments = []
        
        for filepath in self.data_dir.glob("experiment_*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    experiments.append({
                        "filename": filepath.name,
                        "timestamp": data["metadata"]["timestamp"],
                        "problem": data["problem"]["description"]
                    })
            except Exception:
                continue
        
        # Ordena por timestamp (mais recente primeiro)
        experiments.sort(key=lambda x: x["timestamp"], reverse=True)
        return experiments
    
    def get_experiment(self, filename: str) -> Dict[str, Any]:
        """
        Recupera um experimento específico pelo nome do arquivo.
        
        Args:
            filename: Nome do arquivo do experimento
            
        Returns:
            Dados do experimento ou dict com erro
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            return {
                "success": False,
                "error": "Experimento não encontrado"
            }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {
                "success": True,
                "data": data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
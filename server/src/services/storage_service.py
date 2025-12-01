import os
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure, PyMongoError

load_dotenv()

class StorageService:
    """Serviço para armazenar resultados no MongoDB"""
    
    def __init__(self):
        """
        Inicializa o serviço de armazenamento com MongoDB.
        Conecta ao banco de dados 'tcc' e collection 'experiments'.
        """
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            raise ValueError("MONGODB_URI não encontrada no arquivo .env")
        
        try:
            self.client = MongoClient(mongodb_uri)
            # Testa a conexão
            self.client.admin.command('ping')
            
            self.db = self.client['tcc']
            self.collection = self.db['experiments']
            
            # Cria índice no timestamp para ordenação eficiente
            self.collection.create_index([("metadata.timestamp", DESCENDING)])
            
        except ConnectionFailure as e:
            raise ConnectionError(f"Falha ao conectar ao MongoDB: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao inicializar StorageService: {str(e)}")
    
    def save_solver_to_llm_result(
        self,
        problem: str,
        sentences: List[str],
        conclusion: str,
        solver_log: List[str],
        gemini_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Salva o resultado de um experimento no MongoDB.
        
        Args:
            problem: Descrição do problema
            sentences: Lista de sentenças (premissas)
            conclusion: Conclusão do problema
            solver_log: Log de resolução do solver
            gemini_evaluation: Avaliação do Gemini
            
        Returns:
            Dict com informações sobre o documento salvo
        """
        # Gera timestamp e identificador
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        doc_id = f"solver_to_llm_{timestamp_str}"
        
        # Monta o documento
        document = {
            "_id": doc_id,
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "pipeline": "solver_to_llm"
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
        
        # Salva no MongoDB
        try:
            self.collection.insert_one(document)
            
            return {
                "success": True,
                "document_id": doc_id,
                "filename": doc_id  # Mantém compatibilidade com código existente
            }
            
        except PyMongoError as e:
            return {
                "success": False,
                "error": f"Erro ao salvar no MongoDB: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_llm_to_evaluator_result(
        self,
        problem: str,
        sentences: List[str],
        conclusion: str,
        gemini_solution: Dict[str, Any],
        evaluator_log: List[str]
    ) -> Dict[str, Any]:
        """
        Salva o resultado do pipeline: Gemini resolve -> Avaliador avalia no MongoDB.
        
        Args:
            problem: Descrição do problema
            sentences: Lista de sentenças (premissas)
            conclusion: Conclusão do problema
            gemini_solution: Solução gerada pelo Gemini
            evaluator_log: Log de avaliação do evaluator
            
        Returns:
            Dict com informações sobre o documento salvo
        """
        # Gera timestamp e identificador
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        doc_id = f"llm_to_eval_{timestamp_str}"
        
        # Monta o documento
        document = {
            "_id": doc_id,
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "pipeline": "llm_to_evaluator"
            },
            "problem": {
                "description": problem,
                "sentences": sentences,
                "conclusion": conclusion
            },
            "gemini_solution": gemini_solution,
            "evaluator_result": {
                "log": evaluator_log
            }
        }
        
        # Salva no MongoDB
        try:
            self.collection.insert_one(document)
            
            return {
                "success": True,
                "document_id": doc_id,
                "filename": doc_id  # Mantém compatibilidade com código existente
            }
            
        except PyMongoError as e:
            return {
                "success": False,
                "error": f"Erro ao salvar no MongoDB: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_experiments(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de todos os experimentos salvos no MongoDB.
        
        Returns:
            Lista de dicionários com informações dos experimentos
        """
        try:
            # Busca todos os documentos, ordenados por timestamp (mais recente primeiro)
            cursor = self.collection.find(
                {},
                {
                    "_id": 1,
                    "metadata.timestamp": 1,
                    "metadata.pipeline": 1,
                    "problem.description": 1
                }
            ).sort("metadata.timestamp", DESCENDING)
            
            experiments = []
            for doc in cursor:
                experiments.append({
                    "filename": doc["_id"],  # Usa _id como filename para compatibilidade
                    "timestamp": doc["metadata"]["timestamp"],
                    "problem": doc["problem"]["description"],
                    "pipeline": doc["metadata"]["pipeline"]
                })
            
            return experiments
            
        except PyMongoError as e:
            print(f"Erro ao buscar experimentos: {str(e)}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao buscar experimentos: {str(e)}")
            return []
    
    def get_experiment(self, document_id: str) -> Dict[str, Any]:
        """
        Recupera um experimento específico pelo ID do documento.
        
        Args:
            document_id: ID do documento do experimento (equivalente ao filename)
            
        Returns:
            Dados do experimento ou dict com erro
        """
        try:
            document = self.collection.find_one({"_id": document_id})
            
            if not document:
                return {
                    "success": False,
                    "error": "Experimento não encontrado"
                }
            
            # Remove o _id do retorno para evitar problemas de serialização
            doc_data = dict(document)
            doc_data.pop("_id", None)
            
            # Adiciona o _id como filename na metadata para compatibilidade
            if "metadata" not in doc_data:
                doc_data["metadata"] = {}
            doc_data["metadata"]["filename"] = document_id
            
            return {
                "success": True,
                "data": doc_data
            }
            
        except PyMongoError as e:
            return {
                "success": False,
                "error": f"Erro ao buscar experimento: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
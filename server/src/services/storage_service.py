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
        Conecta ao banco de dados 'tcc' e collections 'experiments' e 'problems'.
        """
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            raise ValueError("MONGODB_URI não encontrada no arquivo .env")
        
        try:
            self.client = MongoClient(mongodb_uri)
            # Testa a conexão
            self.client.admin.command('ping')
            
            self.db = self.client['tcc']
            self.experiments_collection = self.db['experimentsnoimpossible']
            self.problems_collection = self.db['problems']
            
            # Cria índices para ordenação eficiente
            self.experiments_collection.create_index([("metadata.timestamp", DESCENDING)])
            self.problems_collection.create_index([("created_at", DESCENDING)])
            self.problems_collection.create_index([("difficulty", 1)])
            
        except ConnectionFailure as e:
            raise ConnectionError(f"Falha ao conectar ao MongoDB: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao inicializar StorageService: {str(e)}")
    
    def save_experiment_result(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Salva um experimento já normalizado no schema padrão.

        Args:
            document: Documento completo do experimento

        Returns:
            Dict com informações sobre o documento salvo
        """
        try:
            doc_data = dict(document)

            if "_id" not in doc_data or not doc_data["_id"]:
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                pipeline = doc_data.get("metadata", {}).get("pipeline", "experiment")
                prefix = "solver_to_llm" if pipeline == "solver_to_llm" else "llm_to_eval" if pipeline == "llm_to_evaluator" else "experiment"
                doc_data["_id"] = f"{prefix}_{timestamp_str}"

            self.experiments_collection.insert_one(doc_data)

            return {
                "success": True,
                "document_id": doc_data["_id"],
                "filename": doc_data["_id"]
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
            cursor = self.experiments_collection.find(
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

    def get_all_experiments_full(self) -> List[Dict[str, Any]]:
        """
        Retorna lista completa de todos os experimentos salvos no MongoDB.

        Returns:
            Lista de documentos completos dos experimentos
        """
        try:
            cursor = self.experiments_collection.find({}).sort("metadata.timestamp", DESCENDING)

            experiments = []
            for doc in cursor:
                doc_data = dict(doc)
                doc_data.pop("_id", None)

                if "metadata" not in doc_data:
                    doc_data["metadata"] = {}
                doc_data["metadata"]["filename"] = doc.get("_id")

                experiments.append(doc_data)

            return experiments

        except PyMongoError as e:
            print(f"Erro ao buscar experimentos completos: {str(e)}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao buscar experimentos completos: {str(e)}")
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
            document = self.experiments_collection.find_one({"_id": document_id})
            
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
    
    # ========== MÉTODOS PARA GERENCIAR PROBLEMAS ==========
    
    def get_all_problems(
        self,
        difficulty: str = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna lista de todos os problemas cadastrados.
        
        Args:
            difficulty: Filtrar por dificuldade (opcional)
            
        Returns:
            Lista de problemas
        """
        try:
            # Monta o filtro
            query = {}
            if difficulty:
                query["difficulty"] = difficulty.lower()
            
            # Busca os documentos
            cursor = self.problems_collection.find(query).sort("created_at", DESCENDING)
            
            problems = []
            for doc in cursor:
                problem = {
                    "id": doc["_id"],
                    "description": doc["description"],
                    "sentences": doc["sentences"],
                    "conclusion": doc["conclusion"],
                    "difficulty": doc["difficulty"],
                    "created_at": doc["created_at"]
                }
                problems.append(problem)
            
            return problems
            
        except PyMongoError as e:
            print(f"Erro ao buscar problemas: {str(e)}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao buscar problemas: {str(e)}")
            return []
    
    def get_problem(self, problem_id: str) -> Dict[str, Any]:
        """
        Recupera um problema específico pelo ID.
        
        Args:
            problem_id: ID do problema
            
        Returns:
            Dados do problema ou dict com erro
        """
        try:
            document = self.problems_collection.find_one({"_id": problem_id})
            
            if not document:
                return {
                    "success": False,
                    "error": "Problema não encontrado"
                }
            
            problem = {
                "id": document["_id"],
                "description": document["description"],
                "sentences": document["sentences"],
                "conclusion": document["conclusion"],
                "difficulty": document["difficulty"],
                "created_at": document["created_at"]
            }
            
            return {
                "success": True,
                "data": problem
            }
            
        except PyMongoError as e:
            return {
                "success": False,
                "error": f"Erro ao buscar problema: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

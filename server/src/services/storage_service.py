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
            self.experiments_collection = self.db['experiments']
            self.problems_collection = self.db['problems']
            
            # Cria índices para ordenação eficiente
            self.experiments_collection.create_index([("metadata.timestamp", DESCENDING)])
            self.problems_collection.create_index([("created_at", DESCENDING)])
            self.problems_collection.create_index([("difficulty", 1)])
            
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
            self.experiments_collection.insert_one(document)
            
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
            self.experiments_collection.insert_one(document)
            
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
    
    def add_problem(
        self,
        description: str,
        sentences: List[str],
        conclusion: str,
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Adiciona um novo problema ao banco de dados.
        
        Args:
            description: Descrição do problema (ex: "p → q, p ⊢ q")
            sentences: Lista de sentenças (premissas)
            conclusion: Conclusão do problema
            difficulty: Dificuldade (easy, medium, hard)
            
        Returns:
            Dict com informações sobre o problema salvo
        """
        # Valida dificuldade
        valid_difficulties = ["easy", "medium", "hard"]
        if difficulty.lower() not in valid_difficulties:
            return {
                "success": False,
                "error": f"Dificuldade inválida. Use: {', '.join(valid_difficulties)}"
            }
        
        # Gera timestamp e ID
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S_%f")
        problem_id = f"problem_{timestamp_str}"
        
        # Monta o documento
        document = {
            "_id": problem_id,
            "description": description,
            "sentences": sentences,
            "conclusion": conclusion,
            "difficulty": difficulty.lower(),
            "created_at": timestamp.isoformat(),
            "usage_count": 0  # Contador de quantas vezes foi usado
        }
        
        try:
            self.problems_collection.insert_one(document)
            
            return {
                "success": True,
                "problem_id": problem_id,
                "message": "Problema cadastrado com sucesso"
            }
            
        except PyMongoError as e:
            return {
                "success": False,
                "error": f"Erro ao salvar problema: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
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
                    "created_at": doc["created_at"],
                    "usage_count": doc.get("usage_count", 0)
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
            
            # Incrementa contador de uso
            self.problems_collection.update_one(
                {"_id": problem_id},
                {"$inc": {"usage_count": 1}}
            )
            
            problem = {
                "id": document["_id"],
                "description": document["description"],
                "sentences": document["sentences"],
                "conclusion": document["conclusion"],
                "difficulty": document["difficulty"],
                "created_at": document["created_at"],
                "usage_count": document.get("usage_count", 0)
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
    
    def delete_problem(self, problem_id: str) -> Dict[str, Any]:
        """
        Remove um problema do banco de dados.
        
        Args:
            problem_id: ID do problema
            
        Returns:
            Dict com resultado da operação
        """
        try:
            result = self.problems_collection.delete_one({"_id": problem_id})
            
            if result.deleted_count == 0:
                return {
                    "success": False,
                    "error": "Problema não encontrado"
                }
            
            return {
                "success": True,
                "message": "Problema removido com sucesso"
            }
            
        except PyMongoError as e:
            return {
                "success": False,
                "error": f"Erro ao remover problema: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
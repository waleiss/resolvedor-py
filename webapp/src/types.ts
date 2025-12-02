export interface Argument {
  sentences: string[];
  conclusion: string;
}

export interface ExperimentMetadata {
  timestamp: string;
  filename: string;
  pipeline: string;
}

export interface ProblemData {
  description: string;
  sentences: string[];
  conclusion: string;
}

export interface GeminiEvaluation {
  success: boolean;
  evaluation: string;
  model: string;
  error?: string;
}

export interface GeminiSolution {
  success: boolean;
  solution: string;
  inferences: string[];
  model: string;
  error?: string;
}

export interface SolverToLLMExperiment {
  metadata: ExperimentMetadata;
  problem: ProblemData;
  solver_result: {
    log: string[];
  };
  gemini_evaluation: GeminiEvaluation;
}

export interface LLMToEvaluatorExperiment {
  metadata: ExperimentMetadata;
  problem: ProblemData;
  gemini_solution: GeminiSolution;
  evaluator_result: {
    log: string[];
  };
}

export type Experiment = SolverToLLMExperiment | LLMToEvaluatorExperiment;

export interface ExperimentListItem {
  filename: string;
  timestamp: string;
  problem: string;
  pipeline: string;
}

export interface SavedProblem {
  id: string;
  description: string;
  sentences: string[];
  conclusion: string;
  difficulty: string;
  created_at: string;
}
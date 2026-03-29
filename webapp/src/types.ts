export interface Argument {
  sentences: string[];
  conclusion: string;
  problem_id?: string;
  difficulty?: string;
}

export type PipelineType = 'solver_to_llm' | 'llm_to_evaluator';

export interface ExperimentMetadata {
  timestamp: string;
  filename: string;
  pipeline: PipelineType;
}

export interface ProblemData {
  problem_id: string;
  description: string;
  sentences: string[];
  conclusion: string;
  difficulty: string;
}

export interface ExperimentAgent {
  type: string;
  model: string;
}

export interface SolverOutput {
  success: boolean;
  steps_raw: string[];
}

export interface EvaluationOutput {
  success: boolean;
  raw_text: string | null;
  log: string[] | null;
  error?: string;
}

export interface Experiment {
  metadata: ExperimentMetadata;
  problem: ProblemData;
  solver: ExperimentAgent;
  evaluator: ExperimentAgent;
  solver_output: SolverOutput;
  evaluation_output: EvaluationOutput;
}

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
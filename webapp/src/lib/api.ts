import type { Argument, ExperimentListItem, Experiment, SavedProblem } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3001';

export async function submitToPipeline1(argument: Argument): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/pipeline1`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(argument),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    
    throw new Error(`HTTP error! status: ${response.status}. Mensagem: ${errorBody}`);
  }

  return response.json();
}

export async function submitToPipeline2(argument: Argument): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/pipeline2`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(argument),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    
    throw new Error(`HTTP error! status: ${response.status}. Mensagem: ${errorBody}`);
  }

  return response.json();
}

export async function getExperiments(): Promise<ExperimentListItem[]> {
  const response = await fetch(`${API_BASE_URL}/experiments`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.experiments;
}

export async function getExperiment(filename: string): Promise<Experiment> {
  const response = await fetch(`${API_BASE_URL}/experiments/${filename}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function getExperimentsWithAnalysis(): Promise<Experiment[]> {
  const response = await fetch(`${API_BASE_URL}/experiments/full`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.experiments;
}

export async function getProblems(): Promise<SavedProblem[]> {
  const response = await fetch(`${API_BASE_URL}/problems`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.problems;
}
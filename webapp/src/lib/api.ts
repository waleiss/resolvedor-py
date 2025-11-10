import type { Argument } from '../types';

const API_BASE_URL = 'http://localhost:3001';

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

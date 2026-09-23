import type { PredictResponse } from '../types';

const API_BASE: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export async function predictImage(file: File): Promise<PredictResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let message = 'Unable to analyze this image. Please upload a valid traffic sign image.';
    try {
      const data = await response.json();
      if (data?.detail) message = data.detail;
    } catch {
      // ignore json parse error
    }
    throw new Error(message);
  }

  return response.json() as Promise<PredictResponse>;
}

export async function checkHealth(): Promise<{ status: string; model_loaded: boolean }> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) throw new Error('Backend unavailable');
  return response.json();
}

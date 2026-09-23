export interface TopPrediction {
  class_id: number;
  name: string;
  confidence: number;
}

export interface PredictResponse {
  prediction: TopPrediction;
  top_predictions: TopPrediction[];
}

export interface UploadState {
  file: File | null;
  previewUrl: string | null;
}

export interface PredictionState {
  result: PredictResponse | null;
  loading: boolean;
  error: string | null;
}

import { useEffect, useState } from 'react';
import { CheckCircle, Award, TrendingUp, AlertCircle } from 'lucide-react';
import type { PredictResponse, TopPrediction } from '../types';

interface PredictionResultProps {
  result: PredictResponse | null;
  error: string | null;
  previewUrl: string | null;
}

// Map confidence to color variant
function confidenceColor(conf: number): string {
  if (conf >= 80) return 'progress-fill-green';
  if (conf >= 50) return 'progress-fill';
  if (conf >= 25) return 'progress-fill-amber';
  return 'progress-fill-red';
}

function ConfidenceBar({ confidence, delay = 0 }: { confidence: number; delay?: number }) {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const t = setTimeout(() => setWidth(confidence), delay + 100);
    return () => clearTimeout(t);
  }, [confidence, delay]);

  return (
    <div className="progress-bar flex-1">
      <div
        className={`progress-fill ${confidenceColor(confidence)}`}
        style={{ width: `${width}%` }}
      />
    </div>
  );
}

function RankBadge({ rank }: { rank: number }) {
  const colors = ['bg-yellow-500/20 text-yellow-400', 'bg-slate-500/20 text-slate-400', 'bg-amber-700/20 text-amber-600'];
  return (
    <span className={`text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center ${colors[rank] ?? 'bg-slate-700 text-slate-500'}`}>
      {rank + 1}
    </span>
  );
}

function TopPredictionRow({ pred, rank }: { pred: TopPrediction; rank: number }) {
  return (
    <div className="flex items-center gap-3 py-2">
      <RankBadge rank={rank} />
      <span className="text-slate-300 text-sm flex-1 truncate">{pred.name}</span>
      <ConfidenceBar confidence={pred.confidence} delay={rank * 120} />
      <span className="text-slate-400 text-sm font-mono w-16 text-right">
        {pred.confidence.toFixed(2)}%
      </span>
    </div>
  );
}

export default function PredictionResult({ result, error, previewUrl }: PredictionResultProps) {
  if (!result && !error) return null;

  return (
    <section id="results" className="py-8 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto animate-slide-up">

      {/* Error state */}
      {error && (
        <div className="glass rounded-3xl p-8 border border-red-500/20 flex items-start gap-4">
          <div className="w-12 h-12 rounded-2xl bg-red-500/20 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-6 h-6 text-red-400" />
          </div>
          <div>
            <h3 className="text-white font-semibold text-lg mb-1">Analysis Failed</h3>
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Success state */}
      {result && (
        <div className="space-y-6">

          {/* Main result card */}
          <div className="glass rounded-3xl p-8 glow-green">
            <div className="flex items-center gap-3 mb-6">
              <CheckCircle className="w-5 h-5 text-emerald-400" />
              <span className="text-emerald-400 font-semibold text-sm uppercase tracking-wider">Prediction</span>
            </div>

            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
              {/* Uploaded image */}
              {previewUrl && (
                <div className="rounded-2xl overflow-hidden bg-surface-900 w-32 h-32 flex-shrink-0 flex items-center justify-center">
                  <img src={previewUrl} alt="Uploaded sign" className="w-full h-full object-contain" />
                </div>
              )}

              {/* Prediction */}
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="badge badge-primary font-mono">Class {result.prediction.class_id}</span>
                </div>
                <h3 className="text-3xl sm:text-4xl font-black text-white mb-3 leading-tight">
                  {result.prediction.name}
                </h3>

                {/* Big confidence bar */}
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-slate-500 text-sm">Confidence</span>
                  <ConfidenceBar confidence={result.prediction.confidence} />
                  <span className={`text-xl font-bold font-mono ${result.prediction.confidence >= 80 ? 'text-emerald-400' : result.prediction.confidence >= 50 ? 'text-primary-400' : 'text-amber-400'}`}>
                    {result.prediction.confidence.toFixed(2)}%
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Top Predictions card */}
          <div className="glass rounded-3xl p-8">
            <div className="flex items-center gap-3 mb-6">
              <Award className="w-5 h-5 text-primary-400" />
              <span className="text-white font-semibold">Top Predictions</span>
            </div>
            <div className="divide-y divide-white/5">
              {result.top_predictions.map((pred, i) => (
                <TopPredictionRow key={pred.class_id} pred={pred} rank={i} />
              ))}
            </div>
          </div>

          {/* Model info strip */}
          <div className="glass rounded-2xl px-6 py-4 flex flex-wrap gap-6 justify-center">
            {[
              { label: 'Model',     value: 'CNN (TensorFlow)' },
              { label: 'Input',     value: '32 × 32 × 3'      },
              { label: 'Classes',   value: '85 Indian Signs' },
              { label: 'Framework', value: 'FastAPI + React'   },
            ].map(({ label, value }) => (
              <div key={label} className="text-center">
                <div className="text-slate-500 text-xs uppercase tracking-wider">{label}</div>
                <div className="text-slate-300 text-sm font-medium font-mono">{value}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

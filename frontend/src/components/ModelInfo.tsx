import { Layers, ArrowDown, Cpu } from 'lucide-react';

const LAYERS = [
  { label: 'Input Image',           detail: '32 × 32 × 3',    color: 'bg-slate-600/20 border-slate-500/30' },
  { label: 'Conv2D Block 1',        detail: '32 Filters',      color: 'bg-blue-600/20 border-blue-500/30'  },
  { label: 'Conv2D Block 2',        detail: '64 Filters',      color: 'bg-indigo-600/20 border-indigo-500/30' },
  { label: 'Conv2D Block 3',        detail: '128 Filters',     color: 'bg-violet-600/20 border-violet-500/30' },
  { label: 'Flatten + Dense',       detail: '512 Units + Dropout 0.5', color: 'bg-purple-600/20 border-purple-500/30' },
  { label: 'Softmax Output',        detail: '85 Classes',      color: 'bg-emerald-600/20 border-emerald-500/30' },
];

const MODEL_STATS = [
  { label: 'Architecture', value: 'CNN (Deep)' },
  { label: 'Classes',       value: '85 Indian Signs' },
  { label: 'Input Size',    value: '32 × 32'    },
  { label: 'Framework',     value: 'Keras 3'    },
  { label: 'Optimizer',     value: 'Adam'       },
  { label: 'Loss',          value: 'Sparse CE'  },
];

export default function ModelInfo() {
  return (
    <section id="model" className="py-24 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">

      {/* Section header */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 badge badge-primary mb-4">
          <Cpu className="w-3.5 h-3.5" />
          Neural Network
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Model Architecture</h2>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          A carefully designed CNN with three convolutional blocks, batch normalization, 
          and dropout for robust traffic sign classification.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">

        {/* Architecture flow */}
        <div className="glass rounded-3xl p-8">
          <div className="flex items-center gap-3 mb-8">
            <Layers className="w-5 h-5 text-primary-400" />
            <span className="text-white font-semibold">Layer Diagram</span>
          </div>

          <div className="flex flex-col items-center gap-0">
            {LAYERS.map((layer, i) => (
              <div key={layer.label} className="flex flex-col items-center w-full">
                <div className={`w-full max-w-xs border rounded-xl px-5 py-3 text-center ${layer.color}`}>
                  <div className="text-white font-semibold text-sm">{layer.label}</div>
                  <div className="text-slate-400 text-xs mt-0.5 font-mono">{layer.detail}</div>
                </div>
                {i < LAYERS.length - 1 && (
                  <div className="flex items-center justify-center my-1">
                    <ArrowDown className="w-4 h-4 text-slate-600" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Model stats + layer details */}
        <div className="space-y-6">

          {/* Stats grid */}
          <div className="glass rounded-3xl p-8">
            <h3 className="text-white font-semibold mb-6">Model Specifications</h3>
            <div className="grid grid-cols-2 gap-4">
              {MODEL_STATS.map(({ label, value }) => (
                <div key={label} className="bg-white/5 rounded-xl p-4">
                  <div className="text-slate-500 text-xs uppercase tracking-wider mb-1">{label}</div>
                  <div className="text-white font-semibold font-mono">{value}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Detailed layer descriptions */}
          <div className="glass rounded-3xl p-8">
            <h3 className="text-white font-semibold mb-6">Architecture Details</h3>
            <div className="space-y-4 text-sm">
              {[
                { title: 'Convolutional Blocks',
                  body: '3 blocks of Conv2D → BatchNorm → Conv2D → MaxPool → Dropout. Each doubles the filter count (32→64→128), capturing increasingly complex features.' },
                { title: 'Activation: ReLU',
                  body: 'Rectified Linear Unit activations in all hidden layers to introduce non-linearity and prevent vanishing gradients.' },
                { title: 'BatchNormalization',
                  body: 'Applied after each Conv2D layer to stabilize training, allow higher learning rates, and reduce internal covariate shift.' },
                { title: 'Dropout (0.5)',
                  body: 'Applied before the output layer to prevent overfitting on the training set.' },
                { title: 'Softmax Output',
                  body: '85-unit Dense layer with Softmax activation producing class probability distributions across all 85 Indian traffic sign categories.' },
              ].map(({ title, body }) => (
                <div key={title} className="border-l-2 border-primary-600/40 pl-4">
                  <div className="text-primary-300 font-medium mb-1">{title}</div>
                  <div className="text-slate-400 leading-relaxed">{body}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

import { Upload, Crop, Brain, Target } from 'lucide-react';

const STEPS = [
  {
    number: '01',
    icon: Upload,
    title: 'Upload',
    desc: 'Drag and drop or browse for any Indian traffic sign image (PNG, JPG, WEBP). The system accepts real-world photos or cropped sign images.',
    color: 'from-blue-600/20 to-indigo-600/10',
    border: 'border-blue-500/20',
    iconColor: 'text-blue-400',
    iconBg: 'bg-blue-500/20',
  },
  {
    number: '02',
    icon: Crop,
    title: 'Preprocess',
    desc: 'The image is automatically resized to 32×32 pixels, converted from BGR to RGB, and normalized to [0, 1] — exactly matching the training pipeline.',
    color: 'from-violet-600/20 to-purple-600/10',
    border: 'border-violet-500/20',
    iconColor: 'text-violet-400',
    iconBg: 'bg-violet-500/20',
  },
  {
    number: '03',
    icon: Brain,
    title: 'CNN Analysis',
    desc: 'The preprocessed image passes through three convolutional blocks with 32, 64, and 128 filters. The network extracts edges, shapes, colors, and sign-specific patterns.',
    color: 'from-primary-600/20 to-indigo-600/10',
    border: 'border-primary-500/20',
    iconColor: 'text-primary-400',
    iconBg: 'bg-primary-500/20',
  },
  {
    number: '04',
    icon: Target,
    title: 'Prediction',
    desc: 'A Softmax layer outputs probabilities for all 85 Indian traffic sign classes. The highest-confidence class is returned with its score and the top-3 predictions.',
    color: 'from-emerald-600/20 to-green-600/10',
    border: 'border-emerald-500/20',
    iconColor: 'text-emerald-400',
    iconBg: 'bg-emerald-500/20',
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 badge badge-primary mb-4">
          <Brain className="w-3.5 h-3.5" />
          Pipeline
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">How It Works</h2>
        <p className="text-slate-400 text-lg max-w-xl mx-auto">
          From image upload to prediction in four clear steps.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {STEPS.map((step, i) => {
          const Icon = step.icon;
          return (
            <div
              key={step.number}
              className={`relative glass rounded-3xl p-6 border ${step.border} bg-gradient-to-b ${step.color} hover:-translate-y-2 transition-transform duration-300`}
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              {/* Step number */}
              <div className="text-6xl font-black text-white/5 absolute top-4 right-4 leading-none select-none">
                {step.number}
              </div>

              {/* Icon */}
              <div className={`w-12 h-12 rounded-2xl ${step.iconBg} flex items-center justify-center mb-5`}>
                <Icon className={`w-6 h-6 ${step.iconColor}`} />
              </div>

              <h3 className="text-white font-bold text-lg mb-3">{step.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{step.desc}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}

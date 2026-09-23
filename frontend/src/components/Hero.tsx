import { ArrowDown, Upload, Play, Shield, Cpu, BarChart3 } from 'lucide-react';

interface HeroProps {
  onUploadClick: () => void;
}

const STATS = [
  { icon: Shield, label: '85 Classes',      desc: 'Indian Sign Categories' },
  { icon: Cpu,    label: 'Deep CNN',        desc: 'TensorFlow / Keras 3'   },
  { icon: BarChart3, label: '88% Val Acc',  desc: '93% Train Accuracy'     },
];

export default function Hero({ onUploadClick }: HeroProps) {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">

      {/* Background */}
      <div className="absolute inset-0 bg-grid opacity-100" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#11111b]" />

      {/* Glow orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-accent-400/8 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center pt-16">

        {/* Badge */}
        <div className="inline-flex items-center gap-2 mb-6 animate-fade-in">
          <span className="badge badge-primary">
            <span className="w-1.5 h-1.5 rounded-full bg-primary-400 animate-pulse" />
            Indian Traffic Sign AI
          </span>
        </div>

        {/* Heading */}
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black leading-tight mb-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          Recognize Traffic Signs
          <br />
          <span className="gradient-text">with Deep Learning</span>
        </h1>

        {/* Subtitle */}
        <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-slide-up" style={{ animationDelay: '0.2s' }}>
          Upload an Indian traffic sign image and let our CNN model — trained on 
          <span className="text-primary-400 font-medium"> 85 Indian traffic sign categories </span>
          — identify the sign in milliseconds with top predictions and confidence scores.
        </p>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16 animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <button onClick={onUploadClick} className="btn-primary text-base px-8 py-4 glow-primary">
            <Upload className="w-5 h-5" />
            Upload Image
          </button>
          <a href="#how-it-works" className="btn-secondary text-base px-8 py-4">
            <Play className="w-5 h-5" />
            How It Works
          </a>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto animate-slide-up" style={{ animationDelay: '0.4s' }}>
          {STATS.map(({ icon: Icon, label, desc }) => (
            <div key={label} className="glass rounded-2xl p-4 text-center hover:border-primary-500/30 transition-all duration-300 hover:-translate-y-1">
              <div className="w-10 h-10 rounded-xl bg-primary-600/20 flex items-center justify-center mx-auto mb-3">
                <Icon className="w-5 h-5 text-primary-400" />
              </div>
              <div className="text-white font-bold text-lg">{label}</div>
              <div className="text-slate-500 text-sm">{desc}</div>
            </div>
          ))}
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce-slow">
          <ArrowDown className="w-5 h-5 text-slate-600" />
        </div>
      </div>
    </section>
  );
}

import { Github, Heart, Zap } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-white/5 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6">

          {/* Brand */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <div>
              <div className="font-bold text-white">TrafficVision</div>
              <div className="text-xs text-slate-500">AI Traffic Sign Recognition</div>
            </div>
          </div>

          {/* Info */}
          <p className="text-slate-500 text-sm text-center">
            CNN trained on{' '}
            <a
              href="https://huggingface.co/datasets/kannanwisen/Indian-Traffic-Sign-Classification"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-400 hover:text-primary-300 transition-colors"
            >
              Indian Traffic Sign Dataset
            </a>
            {' '}· 85 traffic-sign classes · TensorFlow 2.x / Keras 3
          </p>

          {/* Credits */}
          <div className="flex items-center gap-1 text-slate-600 text-sm">
            <span>Built with</span>
            <Heart className="w-3.5 h-3.5 text-red-500 fill-red-500" />
            <span>for Deep Learning</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

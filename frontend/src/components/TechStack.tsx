const TECHS = [
  { name: 'Python 3.11',   desc: 'Backend language',          color: 'border-blue-500/30   bg-blue-500/10   text-blue-400',    emoji: '🐍' },
  { name: 'TensorFlow',    desc: 'Deep learning framework',   color: 'border-orange-500/30 bg-orange-500/10 text-orange-400',  emoji: '🔶' },
  { name: 'Keras',         desc: 'Model building API',        color: 'border-red-500/30    bg-red-500/10    text-red-400',     emoji: '🧠' },
  { name: 'OpenCV',        desc: 'Image processing',          color: 'border-green-500/30  bg-green-500/10  text-green-400',   emoji: '👁️' },
  { name: 'FastAPI',       desc: 'REST API backend',          color: 'border-teal-500/30   bg-teal-500/10   text-teal-400',   emoji: '⚡' },
  { name: 'React 18',      desc: 'Frontend framework',        color: 'border-cyan-500/30   bg-cyan-500/10   text-cyan-400',   emoji: '⚛️' },
  { name: 'TypeScript',    desc: 'Type-safe JavaScript',      color: 'border-blue-400/30   bg-blue-400/10   text-blue-300',   emoji: '📘' },
  { name: 'Tailwind CSS',  desc: 'Utility-first styling',     color: 'border-sky-500/30    bg-sky-500/10    text-sky-400',    emoji: '🎨' },
  { name: 'Vite',          desc: 'Frontend build tool',       color: 'border-purple-500/30 bg-purple-500/10 text-purple-400', emoji: '⚡' },
  { name: 'NumPy',         desc: 'Numerical computing',       color: 'border-indigo-500/30 bg-indigo-500/10 text-indigo-400', emoji: '🔢' },
  { name: 'scikit-learn',  desc: 'ML utilities & metrics',   color: 'border-amber-500/30  bg-amber-500/10  text-amber-400',  emoji: '📊' },
  { name: 'Matplotlib',    desc: 'Training plots',            color: 'border-pink-500/30   bg-pink-500/10   text-pink-400',   emoji: '📈' },
];

export default function TechStack() {
  return (
    <section id="about" className="py-24 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Technology Stack</h2>
        <p className="text-slate-400 text-lg max-w-xl mx-auto">
          Built with a modern, production-grade stack from model training to UI.
        </p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {TECHS.map((tech) => (
          <div
            key={tech.name}
            className={`glass rounded-2xl p-4 border hover:-translate-y-1 transition-all duration-300 hover:shadow-lg ${tech.color}`}
          >
            <div className="text-2xl mb-3">{tech.emoji}</div>
            <div className="text-white font-semibold text-sm mb-1">{tech.name}</div>
            <div className="text-slate-500 text-xs">{tech.desc}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

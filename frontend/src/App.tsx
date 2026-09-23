import { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import ImageUploader from './components/ImageUploader';
import PredictionResult from './components/PredictionResult';
import HowItWorks from './components/HowItWorks';
import ModelInfo from './components/ModelInfo';
import TechStack from './components/TechStack';
import Footer from './components/Footer';
import type { PredictResponse } from './types';

export default function App() {
  const [loading,    setLoading]    = useState(false);
  const [result,     setResult]     = useState<PredictResponse | null>(null);
  const [error,      setError]      = useState<string>('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const scrollToUpload = () => {
    document.getElementById('upload')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleResult = (res: PredictResponse, preview: string) => {
    setResult(res);
    setPreviewUrl(preview);
    setError('');
  };

  const handleError = (msg: string) => {
    if (msg) {
      setError(msg);
      setResult(null);
    }
  };

  return (
    <div className="min-h-screen bg-[#11111b] text-slate-200">
      <Header />

      <main>
        <Hero onUploadClick={scrollToUpload} />

        <div className="section-divider mx-8 sm:mx-16 lg:mx-32" />

        <ImageUploader
          onResult={handleResult}
          onError={handleError}
          loading={loading}
          setLoading={setLoading}
        />

        <PredictionResult
          result={result}
          error={error}
          previewUrl={previewUrl}
        />

        <div className="section-divider mx-8 sm:mx-16 lg:mx-32 mt-8" />

        <HowItWorks />

        <div className="section-divider mx-8 sm:mx-16 lg:mx-32" />

        <ModelInfo />

        <div className="section-divider mx-8 sm:mx-16 lg:mx-32" />

        <TechStack />
      </main>

      <Footer />
    </div>
  );
}

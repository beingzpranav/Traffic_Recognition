import { useRef, useState, useCallback, useEffect } from 'react';
import { Upload, ImageIcon, X, Loader2, AlertCircle, Scan } from 'lucide-react';
import type { PredictResponse } from '../types';
import { predictImage } from '../api/predict';

interface ImageUploaderProps {
  onResult: (result: PredictResponse, previewUrl: string) => void;
  onError: (msg: string) => void;
  loading: boolean;
  setLoading: (v: boolean) => void;
}

const ACCEPTED = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
const MAX_SIZE  = 10 * 1024 * 1024; // 10 MB

export default function ImageUploader({ onResult, onError, loading, setLoading }: ImageUploaderProps) {
  const inputRef   = useRef<HTMLInputElement>(null);
  const [file,     setFile]     = useState<File | null>(null);
  const [preview,  setPreview]  = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);

  // Cleanup object URL on unmount / file change
  useEffect(() => {
    return () => { if (preview) URL.revokeObjectURL(preview); };
  }, [preview]);

  const validate = (f: File): string | null => {
    if (!ACCEPTED.includes(f.type)) return 'Unsupported format. Use PNG, JPG, JPEG, or WEBP.';
    if (f.size > MAX_SIZE)          return 'File too large. Maximum size is 10 MB.';
    return null;
  };

  const handleFile = useCallback((f: File) => {
    const err = validate(f);
    if (err) { setFileError(err); return; }
    setFileError(null);
    setFile(f);
    setPreview(URL.createObjectURL(f));
  }, []);

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  }, [handleFile]);

  const onDragOver = (e: React.DragEvent) => { e.preventDefault(); setDragOver(true);  };
  const onDragLeave = ()                    => { setDragOver(false); };

  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setFileError(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    onError('');
    try {
      const result = await predictImage(file);
      onResult(result, preview ?? '');
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="upload" className="py-20 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
          Analyze a Traffic Sign
        </h2>
        <p className="text-slate-400 text-lg">
          Upload any Indian traffic sign image and our CNN will classify it instantly.
        </p>
      </div>

      <div className="glass rounded-3xl p-6 sm:p-8 glow-primary">

        {/* Drop zone */}
        {!preview ? (
          <div
            className={`drop-zone p-12 flex flex-col items-center justify-center text-center cursor-pointer min-h-[280px] ${dragOver ? 'drag-over' : ''}`}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onClick={() => inputRef.current?.click()}
          >
            <div className={`w-16 h-16 rounded-2xl bg-primary-600/20 flex items-center justify-center mb-5 transition-transform duration-300 ${dragOver ? 'scale-110' : ''}`}>
              <Upload className="w-8 h-8 text-primary-400" />
            </div>
            <h3 className="text-white font-semibold text-xl mb-2">
              Drag &amp; Drop your traffic sign here
            </h3>
            <p className="text-slate-500 mb-6">or</p>
            <button className="btn-secondary text-sm">
              <ImageIcon className="w-4 h-4" />
              Browse Image
            </button>
            <p className="text-slate-600 text-xs mt-6">
              Supports PNG, JPG, JPEG, WEBP · Max 10 MB
            </p>
          </div>
        ) : (
          /* Preview */
          <div className="animate-fade-in">
            <div className="relative rounded-2xl overflow-hidden bg-surface-900 flex items-center justify-center" style={{ minHeight: 280 }}>
              <img
                src={preview}
                alt="Uploaded traffic sign"
                className="max-h-[400px] max-w-full object-contain"
              />
              <button
                onClick={clearFile}
                className="absolute top-3 right-3 w-8 h-8 rounded-full bg-red-500/80 hover:bg-red-500 flex items-center justify-center transition-colors"
                aria-label="Remove image"
              >
                <X className="w-4 h-4 text-white" />
              </button>
              <div className="absolute bottom-3 left-3 badge badge-primary">
                <ImageIcon className="w-3 h-3" />
                {file?.name}
              </div>
            </div>

            {/* Analyze button */}
            <div className="mt-6 flex justify-center">
              <button
                onClick={analyze}
                disabled={loading}
                className="btn-primary px-10 py-4 text-base disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing…
                  </>
                ) : (
                  <>
                    <Scan className="w-5 h-5" />
                    Analyze Traffic Sign
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Validation error */}
        {fileError && (
          <div className="mt-4 flex items-center gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-xl p-3 animate-fade-in">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            {fileError}
          </div>
        )}

        {/* Hidden input */}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED.join(',')}
          className="hidden"
          onChange={onInputChange}
          aria-label="Upload traffic sign image"
        />
      </div>
    </section>
  );
}

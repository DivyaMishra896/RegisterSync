import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadCircular } from '../api/client';

export default function UploadZone({ onUploadComplete }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setError(null);
    setSuccess(null);

    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    try {
      const response = await uploadCircular(file);
      clearInterval(progressInterval);
      setProgress(100);
      setSuccess(response.data);

      setTimeout(() => {
        if (onUploadComplete) {
          onUploadComplete(response.data);
        }
      }, 800);
    } catch (err) {
      clearInterval(progressInterval);
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setProgress(0);
    } finally {
      setUploading(false);
    }
  }, [onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    disabled: uploading,
  });

  if (success) {
    return (
      <div className="upload-zone" style={{ borderColor: 'var(--accent-emerald)', borderStyle: 'solid' }}>
        <CheckCircle size={52} style={{ color: 'var(--accent-emerald)', margin: '0 auto 20px', display: 'block' }} />
        <div className="upload-title" style={{ color: 'var(--accent-emerald)' }}>
          Upload Successful
        </div>
        <div className="upload-subtitle">
          {success.filename} — {success.text_length?.toLocaleString()} characters extracted in {success.num_chunks} chunks
        </div>
        <div style={{ marginTop: '20px' }}>
          <span className="badge badge-verified">Circular ID: {success.circular_id}</span>
        </div>
      </div>
    );
  }

  return (
    <div
      {...getRootProps()}
      className={`upload-zone ${isDragActive ? 'drag-active' : ''}`}
    >
      <input {...getInputProps()} />

      {!uploading ? (
        <>
          <Upload className="upload-icon" size={52} />
          <div className="upload-title">
            {isDragActive ? 'Drop Your Circular Here' : 'Upload RBI / SEBI Circular'}
          </div>
          <div className="upload-subtitle">
            Drag and drop a PDF file, or click to browse
          </div>
          <div style={{ marginTop: '16px' }}>
            <span className="badge" style={{ background: 'var(--bg-tertiary)', color: 'var(--text-tertiary)' }}>
              PDF files only · Max 20MB
            </span>
          </div>
        </>
      ) : (
        <>
          <FileText size={52} style={{ color: 'var(--accent-gold)', margin: '0 auto 20px', display: 'block' }} />
          <div className="upload-title">Processing PDF…</div>
          <div className="upload-subtitle">Extracting text from document</div>
          <div className="upload-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}></div>
            </div>
            <div style={{ marginTop: '8px', fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--text-secondary)', letterSpacing: '0.04em' }}>
              {progress}%
            </div>
          </div>
        </>
      )}

      {error && (
        <div style={{ marginTop: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', color: 'var(--accent-red)' }}>
          <AlertCircle size={16} />
          <span style={{ fontSize: '13px' }}>{error}</span>
        </div>
      )}
    </div>
  );
}

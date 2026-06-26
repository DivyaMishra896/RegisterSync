import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Sparkles, ArrowRight } from 'lucide-react';
import UploadZone from '../components/UploadZone';
import ExtractionView from '../components/ExtractionView';

export default function UploadPage() {
  const navigate = useNavigate();
  const [circularId, setCircularId] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [step, setStep] = useState('upload');

  const handleUploadComplete = (data) => {
    setCircularId(data.circular_id);
    setStep('extract');
  };

  const handleExtract = () => {
    if (!circularId) return;
    setExtracting(true);
  };

  const handleExtractionComplete = () => {
    setStep('done');
    setExtracting(false);
  };

  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="page-title">
          <Upload size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle', opacity: 0.6 }} />
          Upload Circular
        </div>
        <div className="page-subtitle">
          Upload an RBI/SEBI regulatory circular to extract compliance requirements
        </div>
      </div>

      <div className="page-content">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '32px',
          padding: '20px 0',
          borderBottom: '1px solid var(--border-color)',
        }}>
          <StepIndicator number={1} label="Upload PDF" active={step === 'upload'} completed={step !== 'upload'} />
          <div style={{ width: '40px', height: '1px', background: 'var(--border-color)' }} />
          <StepIndicator number={2} label="AI Extraction" active={step === 'extract' || extracting} completed={step === 'done'} />
          <div style={{ width: '40px', height: '1px', background: 'var(--border-color)' }} />
          <StepIndicator number={3} label="Review & Dashboard" active={step === 'done'} completed={false} />
        </div>

        {step === 'upload' && (
          <UploadZone onUploadComplete={handleUploadComplete} />
        )}

        {step === 'extract' && !extracting && (
          <div className="card" style={{ textAlign: 'center', padding: '56px 40px', borderTop: '2px solid var(--accent-gold)' }}>
            <Sparkles size={44} style={{ color: 'var(--accent-gold)', margin: '0 auto 20px', display: 'block' }} />
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '22px', fontWeight: 600, marginBottom: '10px' }}>
              PDF Uploaded Successfully
            </div>
            <div style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '28px', maxWidth: '480px', margin: '0 auto 28px', lineHeight: '1.7' }}>
              Ready to extract rules using AI. Watch the Multi-Agent system analyze the document, 
              extract compliance requirements, and check for conflicts in real-time.
            </div>
            
            <button className="btn btn-primary btn-lg" onClick={handleExtract}>
              <Sparkles size={18} />
              Extract Rules with AI
            </button>
          </div>
        )}

        {(extracting || step === 'done') && circularId && (
          <ExtractionView 
            circularId={circularId} 
            isStreaming={extracting}
            onComplete={handleExtractionComplete} 
          />
        )}

        {step === 'done' && (
          <div style={{ marginTop: '28px', textAlign: 'center' }}>
            <button className="btn btn-primary btn-lg" onClick={() => navigate('/dashboard')}>
              <ArrowRight size={18} />
              View Compliance Dashboard
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function StepIndicator({ number, label, active, completed }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      opacity: active || completed ? 1 : 0.35,
      transition: 'all 200ms ease-out',
    }}>
      <div style={{
        width: '30px',
        height: '30px',
        borderRadius: '50%',
        background: completed
          ? 'var(--accent-emerald)'
          : active
          ? 'var(--accent-blue)'
          : 'var(--bg-tertiary)',
        border: completed || active ? 'none' : '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '12px',
        fontWeight: 600,
        fontFamily: 'var(--font-mono)',
        color: completed || active ? '#fff' : 'var(--text-tertiary)',
        transition: 'all 200ms ease-out',
      }}>
        {completed ? '✓' : number}
      </div>
      <span style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '11px',
        fontWeight: 500,
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
        color: active ? 'var(--text-primary)' : 'var(--text-secondary)',
      }}>
        {label}
      </span>
    </div>
  );
}

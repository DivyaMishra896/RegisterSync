import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Sparkles, ArrowRight } from 'lucide-react';
import UploadZone from '../components/UploadZone';
import ExtractionView from '../components/ExtractionView';
import { triggerExtraction } from '../api/client';

export default function UploadPage() {
  const navigate = useNavigate();
  const [circularId, setCircularId] = useState(null);
  const [extractionData, setExtractionData] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [step, setStep] = useState('upload'); // upload, extract, done

  const handleUploadComplete = (data) => {
    setCircularId(data.circular_id);
    setStep('extract');
  };

  const handleExtract = async () => {
    if (!circularId) return;
    setExtracting(true);

    try {
      const response = await triggerExtraction(circularId);
      setExtractionData(response.data);
      setStep('done');
    } catch (err) {
      console.error('Extraction failed:', err);
    } finally {
      setExtracting(false);
    }
  };

  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="page-title">
          <Upload size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
          Upload Circular
        </div>
        <div className="page-subtitle">
          Upload an RBI/SEBI regulatory circular to extract compliance requirements
        </div>
      </div>

      <div className="page-content">
        {/* Step Indicator */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '28px',
        }}>
          <StepIndicator number={1} label="Upload PDF" active={step === 'upload'} completed={step !== 'upload'} />
          <ArrowRight size={16} style={{ color: 'var(--text-tertiary)' }} />
          <StepIndicator number={2} label="AI Extraction" active={step === 'extract' || extracting} completed={step === 'done'} />
          <ArrowRight size={16} style={{ color: 'var(--text-tertiary)' }} />
          <StepIndicator number={3} label="Review & Dashboard" active={step === 'done'} completed={false} />
        </div>

        {/* Upload Step */}
        {step === 'upload' && (
          <UploadZone onUploadComplete={handleUploadComplete} />
        )}

        {/* Extract Step */}
        {step === 'extract' && !extracting && !extractionData && (
          <div className="card" style={{ textAlign: 'center', padding: '50px' }}>
            <Sparkles size={48} style={{ color: 'var(--accent-purple)', margin: '0 auto 16px', display: 'block' }} />
            <div style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>
              PDF uploaded successfully!
            </div>
            <div style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Ready to extract rules using AI. This will analyze the document, extract compliance requirements,
              generate action items, and check for conflicts with existing rules.
            </div>
            <button className="btn btn-primary btn-lg" onClick={handleExtract}>
              <Sparkles size={18} />
              Extract Rules with AI
            </button>
          </div>
        )}

        {/* Extracting / Results */}
        {(extracting || extractionData) && (
          <ExtractionView extractionData={extractionData} loading={extracting} />
        )}

        {/* Go to Dashboard */}
        {step === 'done' && (
          <div style={{ marginTop: '24px', textAlign: 'center' }}>
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
      gap: '8px',
      opacity: active || completed ? 1 : 0.4,
    }}>
      <div style={{
        width: '28px',
        height: '28px',
        borderRadius: '50%',
        background: completed
          ? 'var(--accent-emerald)'
          : active
          ? 'var(--accent-purple)'
          : 'var(--bg-tertiary)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '12px',
        fontWeight: 700,
        color: completed || active ? '#fff' : 'var(--text-tertiary)',
        transition: 'all var(--transition-base)',
      }}>
        {completed ? '✓' : number}
      </div>
      <span style={{
        fontSize: '13px',
        fontWeight: active ? 600 : 400,
        color: active ? 'var(--text-primary)' : 'var(--text-secondary)',
      }}>
        {label}
      </span>
    </div>
  );
}

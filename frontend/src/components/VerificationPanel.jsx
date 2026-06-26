import { useState } from 'react';
import { Shield, Play, CheckCircle, XCircle, AlertCircle, Clock, FileText } from 'lucide-react';
import { runVerification } from '../api/client';

export default function VerificationPanel({ onVerificationComplete }) {
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleRunVerification = async () => {
    setRunning(true);
    setError(null);

    try {
      const response = await runVerification();
      setResults(response.data.results);

      if (onVerificationComplete) {
        onVerificationComplete(response.data.results);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Verification failed');
    } finally {
      setRunning(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Verified': return <CheckCircle size={16} style={{ color: 'var(--status-verified)' }} />;
      case 'Failed': return <XCircle size={16} style={{ color: 'var(--status-failed)' }} />;
      case 'Partially Done': return <AlertCircle size={16} style={{ color: 'var(--status-partial)' }} />;
      default: return <Clock size={16} style={{ color: 'var(--status-pending)' }} />;
    }
  };

  return (
    <div className="verification-panel">
      <div className="verification-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--accent-blue-dim)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <Shield size={20} style={{ color: 'var(--accent-blue)' }} />
          </div>
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '17px', fontWeight: 600 }}>Verification Agent</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--text-tertiary)', letterSpacing: '0.08em', textTransform: 'uppercase', marginTop: '2px' }}>
              Reads system logs to auto-verify compliance
            </div>
          </div>
        </div>

        <button
          className={`btn ${running ? 'btn-outline' : 'btn-success'}`}
          onClick={handleRunVerification}
          disabled={running}
        >
          {running ? (
            <>
              <div className="spinner"></div>
              Scanning Logs…
            </>
          ) : (
            <>
              <Play size={16} />
              Run Verification
            </>
          )}
        </button>
      </div>

      {error && (
        <div style={{ padding: '12px 16px', background: 'var(--accent-red-dim)', borderRadius: 'var(--radius-md)', color: 'var(--accent-red)', fontSize: '13px', marginBottom: '16px', border: '1px solid rgba(198, 40, 40, 0.12)' }}>
          {error}
        </div>
      )}

      {results && (
        <>
          <div className="verification-stats">
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--text-primary)' }}>{results.total_checked}</div>
              <div className="stat-label">Checked</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--status-verified)' }}>{results.verified}</div>
              <div className="stat-label">Verified</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--status-failed)' }}>{results.failed}</div>
              <div className="stat-label">Failed</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--status-partial)' }}>{results.partially_done}</div>
              <div className="stat-label">Partial</div>
            </div>
          </div>

          <div style={{ fontFamily: 'var(--font-display)', fontSize: '15px', fontWeight: 600, marginBottom: '14px' }}>
            Verification Log
          </div>
          <div className="verification-timeline">
            {results.details?.map((detail, i) => (
              <div key={i} className="verification-event">
                <div className={`verification-event-dot ${detail.new_status?.toLowerCase().replace(' ', '-')}`}>
                  {getStatusIcon(detail.new_status)}
                </div>
                <div className="verification-event-content">
                  <div className="verification-event-title">
                    {detail.task_ref} — {detail.new_status}
                  </div>
                  <div className="verification-event-desc">
                    {detail.title?.replace(/^\[.*?\]\s*/, '')}
                  </div>
                  {detail.evidence && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
                      <FileText size={11} style={{ color: 'var(--accent-emerald)' }} />
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--accent-emerald)', letterSpacing: '0.04em' }}>{detail.evidence}</span>
                    </div>
                  )}
                  {detail.note && (
                    <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginTop: '4px', fontStyle: 'italic', lineHeight: '1.5' }}>
                      {detail.note}
                    </div>
                  )}
                  {detail.timestamp && (
                    <div className="verification-event-time">{detail.timestamp}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

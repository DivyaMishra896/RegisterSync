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
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--accent-emerald-dim)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <Shield size={20} style={{ color: 'var(--accent-emerald)' }} />
          </div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 600 }}>Verification Agent</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Reads system logs to auto-verify task compliance
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
              Scanning Logs...
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
        <div style={{ padding: '12px 16px', background: 'var(--accent-red-dim)', borderRadius: 'var(--radius-md)', color: 'var(--accent-red)', fontSize: '13px', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      {results && (
        <>
          {/* Stats */}
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

          {/* Timeline */}
          <div style={{ fontSize: '14px', fontWeight: 600, marginBottom: '12px' }}>
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
                      <FileText size={12} style={{ color: 'var(--accent-emerald)' }} />
                      <span style={{ fontSize: '11px', color: 'var(--accent-emerald)' }}>{detail.evidence}</span>
                    </div>
                  )}
                  {detail.note && (
                    <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginTop: '4px', fontStyle: 'italic' }}>
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

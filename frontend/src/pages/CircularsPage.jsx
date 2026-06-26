import { useState, useEffect } from 'react';
import { FileText, Calendar, Hash, ExternalLink } from 'lucide-react';
import { getCirculars } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function CircularsPage() {
  const [circulars, setCirculars] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCirculars = async () => {
      try {
        const response = await getCirculars();
        setCirculars(response.data.circulars || []);
      } catch (err) {
        console.error('Failed to fetch circulars:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCirculars();
  }, []);

  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="page-title">
          <FileText size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle', opacity: 0.6 }} />
          Uploaded Circulars
        </div>
        <div className="page-subtitle">View all uploaded regulatory circulars and their processing status</div>
      </div>

      <div className="page-content">
        <div className="section-label">
          <span>Document Registry</span>
        </div>

        {loading ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[1, 2, 3].map(i => (
              <div key={i} className="card">
                <div className="skeleton" style={{ width: '200px', height: '18px', marginBottom: '8px' }}></div>
                <div className="skeleton" style={{ width: '300px', height: '12px' }}></div>
              </div>
            ))}
          </div>
        ) : circulars.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📄</div>
            <div className="empty-state-title">No Circulars Uploaded</div>
            <div className="empty-state-text">
              Go to the Upload page to upload your first regulatory circular.
            </div>
            <button className="btn btn-primary" style={{ marginTop: '20px' }} onClick={() => navigate('/upload')}>
              Upload Circular
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {circulars.map(circular => (
              <div key={circular.id} className="card" style={{ cursor: 'pointer' }} onClick={() => navigate(`/upload`)}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: 'var(--radius-md)',
                      background: 'var(--accent-blue-dim)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '20px',
                    }}>
                      📄
                    </div>
                    <div>
                      <div style={{ fontFamily: 'var(--font-display)', fontSize: '16px', fontWeight: 600, marginBottom: '4px' }}>
                        {circular.filename}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '11px', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)', letterSpacing: '0.04em' }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Calendar size={11} />
                          {circular.upload_date ? new Date(circular.upload_date).toLocaleDateString() : 'N/A'}
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Hash size={11} />
                          {circular.source}
                        </span>
                        <span>
                          {circular.rule_count} rules · {circular.task_count} tasks
                        </span>
                      </div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span className={`badge ${circular.status === 'processed' ? 'badge-verified' : circular.status === 'error' ? 'badge-failed' : 'badge-pending'}`}>
                      {circular.status}
                    </span>
                    <ExternalLink size={15} style={{ color: 'var(--text-tertiary)' }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

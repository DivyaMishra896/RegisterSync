import { useState, useEffect, useRef } from 'react';
import { Brain, Loader2, Sparkles, ArrowRight, Terminal } from 'lucide-react';
import StatusBadge, { PriorityBadge, DepartmentBadge } from './StatusBadge';
import { API_BASE, getRules, getConflicts, getTasks } from '../api/client';

export default function ExtractionView({ circularId, isStreaming, onComplete }) {
  const [logs, setLogs] = useState([]);
  const [extractionData, setExtractionData] = useState(null);
  const [error, setError] = useState(null);
  const [nonRegulatory, setNonRegulatory] = useState(false);
  const logEndRef = useRef(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  useEffect(() => {
    if (isStreaming || extractionData || !circularId) return;

    const fetchSavedResults = async () => {
      try {
        setLogs([{ agent: 'System', thought: 'Loading previously extracted results...' }]);
        const [rulesRes, conflictsRes, tasksRes] = await Promise.all([
          getRules(circularId),
          getConflicts(circularId),
          getTasks({ circular_id: circularId }),
        ]);

        const rules = rulesRes.data.rules || [];
        const conflicts = conflictsRes.data.conflicts || [];
        const tasks = tasksRes.data.tasks || [];

        if (rules.length === 0 && tasks.length === 0) {
          setLogs(prev => [...prev, { agent: 'System', thought: 'No extraction data found for this circular.' }]);
          return;
        }

        setExtractionData({
          rules_extracted: rules.length,
          tasks_generated: tasks.length,
          conflicts_found: conflicts.length,
          rules,
          conflicts,
          tasks,
        });
        setLogs(prev => [...prev, { agent: 'System', thought: 'Results loaded successfully.' }]);
      } catch (err) {
        console.error('Failed to load saved extraction results:', err);
        setLogs(prev => [...prev, { agent: 'System', thought: 'Could not reload extraction results.' }]);
      }
    };

    fetchSavedResults();
  }, [circularId, isStreaming]);

  useEffect(() => {
    if (!isStreaming) return;

    setLogs([{ agent: 'System', thought: 'Initializing Multi-Agent Orchestrator...' }]);
    
    const eventSource = new EventSource(`${API_BASE}/extract/${circularId}/stream`);

    eventSource.addEventListener('thought', (e) => {
      try {
        const data = JSON.parse(e.data);
        setLogs(prev => [...prev, data]);
      } catch (err) {
        console.error('Error parsing thought:', err);
      }
    });

    let isFinished = false;

    eventSource.addEventListener('non_regulatory', (e) => {
      isFinished = true;
      eventSource.close();
      setNonRegulatory(true);
      setLogs(prev => [...prev, {
        agent: 'Orchestrator',
        thought: 'Document rejected: not a regulatory circular. No rules will be extracted.',
      }]);
      if (onComplete) onComplete();
    });

    eventSource.addEventListener('complete', async (e) => {
      isFinished = true;
      eventSource.close();
      
      try {
        const stats = JSON.parse(e.data);
        setLogs(prev => [...prev, { agent: 'System', thought: 'Pipeline complete. Fetching final results...' }]);
        
        const [rulesRes, conflictsRes, tasksRes] = await Promise.all([
          getRules(circularId),
          getConflicts(circularId),
          getTasks({ circular_id: circularId })
        ]);

        setExtractionData({
          ...stats,
          rules: rulesRes.data.rules,
          conflicts: conflictsRes.data.conflicts,
          tasks: tasksRes.data.tasks || []
        });
        
        if (onComplete) onComplete();
      } catch (err) {
        console.error('Error completing extraction:', err);
        setError('Failed to load final results.');
      }
    });

    eventSource.addEventListener('error', (e) => {
      if (isFinished) return;
      
      let msg = 'SSE connection error (Server may have closed the connection)';
      if (e.data) msg = e.data;
      setError(msg);
      eventSource.close();
      if (onComplete) onComplete();
    });

    return () => {
      eventSource.close();
    };
  }, [isStreaming, circularId]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {nonRegulatory && (
        <div style={{
          padding: '20px 24px',
          borderRadius: 'var(--radius-lg)',
          background: 'rgba(198, 40, 40, 0.05)',
          border: '1px solid var(--accent-red-dim)',
          borderLeft: '3px solid var(--accent-red)',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '14px',
        }}>
          <span style={{ fontSize: '22px', flexShrink: 0 }}>⚠️</span>
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: '15px', fontWeight: 600, color: 'var(--accent-red)', marginBottom: '4px' }}>
              Non-Regulatory Document
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              This PDF does not appear to be an RBI/SEBI regulatory circular.
              No rules or MAP tasks were generated.
              Please upload a genuine regulatory circular.
            </div>
          </div>
        </div>
      )}
      <div className="card" style={{ 
        background: '#1C1C1E', 
        color: '#E5E5EA', 
        border: '1px solid #2C2C2E',
        borderTop: '2px solid var(--accent-gold)',
        padding: 0,
      }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '8px', 
          padding: '14px 20px', 
          borderBottom: '1px solid #2C2C2E', 
          background: '#1C1C1E',
        }}>
          <Terminal size={14} style={{ color: 'var(--accent-gold)' }} />
          <span style={{ 
            fontFamily: 'var(--font-mono)', 
            fontSize: '10px', 
            fontWeight: 500, 
            color: 'var(--accent-gold)', 
            letterSpacing: '0.15em',
            textTransform: 'uppercase',
          }}>Agent Reasoning Log</span>
          {isStreaming && <Loader2 size={13} style={{ marginLeft: 'auto', color: 'var(--accent-gold)', animation: 'spin 2s linear infinite' }} />}
        </div>
        <div style={{ 
          padding: '16px 20px', 
          height: '240px', 
          overflowY: 'auto', 
          fontFamily: 'var(--font-mono)', 
          fontSize: '12px', 
          lineHeight: '1.7',
          letterSpacing: '0.02em',
        }}>
          {logs.map((log, i) => (
            <div key={i} style={{ marginBottom: '6px', display: 'flex', gap: '8px' }}>
              <span style={{ color: getAgentColor(log.agent), fontWeight: 600, minWidth: '100px', fontSize: '11px' }}>
                [{log.agent}]
              </span>
              <span style={{ opacity: 0.85, color: '#E5E5EA' }}>{log.thought}</span>
            </div>
          ))}
          {error && <div style={{ color: '#FF6B6B', marginTop: '12px' }}>Error: {error}</div>}
          <div ref={logEndRef} />
        </div>
      </div>

      {extractionData && (
        <ExtractionResults data={extractionData} />
      )}
    </div>
  );
}

function getAgentColor(agent) {
  switch(agent) {
    case 'Orchestrator': return '#B8860B';
    case 'Reader': return '#569cd6';
    case 'Extractor': return '#4ec9b0';
    case 'Conflict': return '#d16969';
    case 'Router': return '#ce9178';
    default: return '#8E8E93';
  }
}

function ExtractionResults({ data }) {
  return (
    <div>
      <div className="section-label">
        <span>Extraction Results</span>
      </div>

      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: '28px' }}>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: 'var(--accent-blue-dim)', color: 'var(--accent-blue)' }}>📋</div>
          <div className="stat-value">{data.rules_extracted}</div>
          <div className="stat-label">Rules Extracted</div>
        </div>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: 'var(--accent-gold-dim)', color: 'var(--accent-gold)' }}>✅</div>
          <div className="stat-value">{data.tasks_generated}</div>
          <div className="stat-label">MAPs Generated</div>
        </div>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: data.conflicts_found > 0 ? 'var(--accent-red-dim)' : 'var(--accent-emerald-dim)', color: data.conflicts_found > 0 ? 'var(--accent-red)' : 'var(--accent-emerald)' }}>
            {data.conflicts_found > 0 ? '⚠️' : '✓'}
          </div>
          <div className="stat-value">{data.conflicts_found}</div>
          <div className="stat-label">Conflicts Found</div>
        </div>
      </div>

      {data.conflicts && data.conflicts.length > 0 && (
        <div style={{ marginBottom: '28px' }}>
          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '18px', fontWeight: 600, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            ⚠️ Regulatory Diff: Conflict Analysis
          </h3>
          {data.conflicts.map((conflict, i) => (
            <div key={i} className="card" style={{ marginBottom: '16px', border: '1px solid var(--accent-red-dim)', background: 'rgba(198,40,40,0.02)', borderTop: '2px solid var(--accent-red)' }}>
              <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className={`badge ${conflict.severity === 'High' ? 'badge-high' : 'badge-medium'}`}>
                    {conflict.severity} Severity
                  </span>
                  <span className={`conflict-alert-type ${conflict.conflict_type?.toLowerCase()}`}>
                    {conflict.conflict_type}
                  </span>
                </div>
              </div>
              <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border-color)', fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                <strong>Agent Analysis:</strong> {conflict.reason}
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1px', background: 'var(--border-color)' }}>
                <div style={{ padding: '16px', background: 'var(--bg-secondary)' }}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', fontWeight: 500, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: '8px' }}>
                    EXISTING RULE (OLD)
                  </div>
                  <div style={{ fontFamily: 'var(--font-display)', fontSize: '14px', fontWeight: 500, color: 'var(--text-primary)' }}>
                    <span style={{ color: 'var(--accent-red)', fontWeight: 800, marginRight: '8px' }}>−</span>
                    {conflict.existing_rule_title}
                  </div>
                </div>
                
                <div style={{ padding: '16px', background: 'var(--bg-secondary)' }}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', fontWeight: 500, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: '8px' }}>
                    NEW CIRCULAR (NEW)
                  </div>
                  <div style={{ fontFamily: 'var(--font-display)', fontSize: '14px', fontWeight: 500, color: 'var(--text-primary)' }}>
                    <span style={{ color: 'var(--accent-emerald)', fontWeight: 800, marginRight: '8px' }}>+</span>
                    {conflict.new_rule_title}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="extraction-container">
        <div className="extraction-panel">
          <div className="extraction-panel-header">
            <Brain size={16} style={{ color: 'var(--accent-blue)' }} />
            Extracted Rules
          </div>
          <div className="extraction-panel-body">
            {data.rules?.map((rule, index) => (
              <div key={rule.rule_id || index} className="rule-card">
                <div className="rule-card-header">
                  <span className="rule-id">{rule.rule_id}</span>
                  <PriorityBadge priority={rule.priority} />
                </div>
                <div className="rule-title">{rule.title}</div>
                <div className="rule-description">{rule.description}</div>
                <div className="rule-meta">
                  {rule.affected_departments?.map((dept, j) => (
                    <DepartmentBadge key={j} department={dept} />
                  ))}
                  {rule.deadline && (
                    <span className="badge" style={{ background: 'var(--bg-tertiary)', color: 'var(--text-tertiary)' }}>
                      📅 {rule.deadline}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="extraction-panel">
          <div className="extraction-panel-header">
            <Sparkles size={16} style={{ color: 'var(--accent-gold)' }} />
            Generated MAPs
          </div>
          <div className="extraction-panel-body">
            {data.tasks?.map((task, index) => (
              <div key={task.task_ref || index} className="rule-card">
                <div className="rule-card-header">
                  <span className="rule-id">{task.task_ref}</span>
                  <StatusBadge status={task.status} />
                </div>
                <div className="rule-title" style={{ fontSize: '14px' }}>{task.title}</div>
                <div className="rule-meta" style={{ marginTop: '8px' }}>
                  <DepartmentBadge department={task.department} />
                  <PriorityBadge priority={task.priority} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState, useEffect, useRef } from 'react';
import { Brain, Loader2, Sparkles, ArrowRight, Terminal } from 'lucide-react';
import StatusBadge, { PriorityBadge, DepartmentBadge } from './StatusBadge';
import { API_BASE, getRules, getConflicts, getTasks } from '../api/client';

export default function ExtractionView({ circularId, isStreaming, onComplete }) {
  const [logs, setLogs] = useState([]);
  const [extractionData, setExtractionData] = useState(null);
  const [error, setError] = useState(null);
  const logEndRef = useRef(null);

  // Auto-scroll logs
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

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

    eventSource.addEventListener('complete', async (e) => {
      isFinished = true;
      eventSource.close(); // Close immediately to prevent reconnection/error events
      
      try {
        const stats = JSON.parse(e.data);
        setLogs(prev => [...prev, { agent: 'System', thought: 'Pipeline complete. Fetching final results...' }]);
        
        // Fetch the generated data
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
      if (isFinished) return; // Ignore disconnect errors after we already finished
      
      // If data is passed in the error event
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
      {/* Agent Reasoning Log Panel */}
      <div className="card" style={{ background: '#1e1e1e', color: '#d4d4d4', border: '1px solid #333' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 16px', borderBottom: '1px solid #333', background: '#252526' }}>
          <Terminal size={16} style={{ color: 'var(--accent-purple)' }} />
          <span style={{ fontSize: '13px', fontWeight: 600, color: '#fff', letterSpacing: '0.5px' }}>AGENT REASONING LOG</span>
          {isStreaming && <Loader2 size={14} style={{ marginLeft: 'auto', color: 'var(--accent-amber)', animation: 'spin 2s linear infinite' }} />}
        </div>
        <div style={{ padding: '16px', height: '240px', overflowY: 'auto', fontFamily: 'monospace', fontSize: '13px', lineHeight: '1.6' }}>
          {logs.map((log, i) => (
            <div key={i} style={{ marginBottom: '8px', display: 'flex', gap: '8px' }}>
              <span style={{ color: getAgentColor(log.agent), fontWeight: 'bold', minWidth: '100px' }}>
                [{log.agent}]
              </span>
              <span style={{ opacity: 0.9 }}>{log.thought}</span>
            </div>
          ))}
          {error && <div style={{ color: '#f87171', marginTop: '12px' }}>Error: {error}</div>}
          <div ref={logEndRef} />
        </div>
      </div>

      {/* Results Section */}
      {extractionData && (
        <ExtractionResults data={extractionData} />
      )}
    </div>
  );
}

function getAgentColor(agent) {
  switch(agent) {
    case 'Orchestrator': return '#c586c0'; // purple
    case 'Reader': return '#569cd6'; // blue
    case 'Extractor': return '#4ec9b0'; // teal
    case 'Conflict': return '#d16969'; // red
    case 'Router': return '#ce9178'; // orange
    default: return '#808080';
  }
}

// Extracted the results UI into a sub-component to keep it clean
function ExtractionResults({ data }) {
  return (
    <div>
      {/* Summary Stats */}
      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: '24px' }}>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: 'var(--accent-purple-dim)', color: 'var(--accent-purple)' }}>📋</div>
          <div className="stat-value">{data.rules_extracted}</div>
          <div className="stat-label">Rules Extracted</div>
        </div>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: 'var(--accent-blue-dim)', color: 'var(--accent-blue)' }}>✅</div>
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

      {/* Conflicts / Regulatory Diff */}
      {data.conflicts && data.conflicts.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            ⚠️ Regulatory Diff: Conflict Analysis
          </h3>
          {data.conflicts.map((conflict, i) => (
            <div key={i} className="card" style={{ marginBottom: '16px', border: '1px solid var(--accent-red-dim)', background: 'rgba(248,113,113,0.03)' }}>
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
              <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border-color)', fontSize: '13px', color: 'var(--text-secondary)' }}>
                <strong>Agent Analysis:</strong> {conflict.reason}
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1px', background: 'var(--border-color)' }}>
                {/* Old Rule */}
                <div style={{ padding: '16px', background: 'var(--bg-secondary)' }}>
                  <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '8px' }}>
                    EXISTING RULE (OLD)
                  </div>
                  <div style={{ fontSize: '14px', fontWeight: 500, color: 'var(--text-primary)' }}>
                    <span style={{ color: 'var(--accent-red)', fontWeight: 800, marginRight: '8px' }}>-</span>
                    {conflict.existing_rule_title}
                  </div>
                </div>
                
                {/* New Rule */}
                <div style={{ padding: '16px', background: 'var(--bg-secondary)' }}>
                  <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '8px' }}>
                    NEW CIRCULAR (NEW)
                  </div>
                  <div style={{ fontSize: '14px', fontWeight: 500, color: 'var(--text-primary)' }}>
                    <span style={{ color: 'var(--accent-emerald)', fontWeight: 800, marginRight: '8px' }}>+</span>
                    {conflict.new_rule_title}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Rules Grid */}
      <div className="extraction-container">
        <div className="extraction-panel">
          <div className="extraction-panel-header">
            <Brain size={16} style={{ color: 'var(--accent-purple)' }} />
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

        {/* Generated Tasks */}
        <div className="extraction-panel">
          <div className="extraction-panel-header">
            <Sparkles size={16} style={{ color: 'var(--accent-emerald)' }} />
            Generated MAPs
          </div>
          <div className="extraction-panel-body">
            {data.tasks?.map((task, index) => (
              <div key={task.task_ref || index} className="rule-card">
                <div className="rule-card-header">
                  <span className="rule-id">{task.task_ref}</span>
                  <StatusBadge status={task.status} />
                </div>
                <div className="rule-title" style={{ fontSize: '13px' }}>{task.title}</div>
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

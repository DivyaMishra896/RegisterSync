import { useState, useEffect } from 'react';
import { Brain, Loader2, Sparkles, ArrowRight } from 'lucide-react';
import StatusBadge, { PriorityBadge, DepartmentBadge } from './StatusBadge';

export default function ExtractionView({ extractionData, loading }) {
  const [visibleRules, setVisibleRules] = useState([]);
  const [visibleTasks, setVisibleTasks] = useState([]);

  useEffect(() => {
    if (extractionData?.rules) {
      // Animate rules appearing one by one
      extractionData.rules.forEach((rule, index) => {
        setTimeout(() => {
          setVisibleRules(prev => [...prev, rule]);
        }, index * 400);
      });
    }
  }, [extractionData?.rules]);

  useEffect(() => {
    if (extractionData?.tasks) {
      const rulesDelay = (extractionData?.rules?.length || 0) * 400 + 500;
      extractionData.tasks.forEach((task, index) => {
        setTimeout(() => {
          setVisibleTasks(prev => [...prev, task]);
        }, rulesDelay + index * 300);
      });
    }
  }, [extractionData?.tasks, extractionData?.rules?.length]);

  if (loading) {
    return (
      <div className="extraction-container" style={{ display: 'block' }}>
        <div className="card" style={{ textAlign: 'center', padding: '60px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '16px' }}>
            <Brain size={32} style={{ color: 'var(--accent-purple)', animation: 'spin 2s linear infinite' }} />
            <Sparkles size={20} style={{ color: 'var(--accent-amber)', animation: 'pulse-dot 1.5s ease-in-out infinite' }} />
          </div>
          <div style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>
            AI is analyzing the circular...
          </div>
          <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
            Extracting rules, generating MAPs, and checking for conflicts
          </div>
          <div style={{ marginTop: '24px' }}>
            <div className="progress-bar" style={{ maxWidth: '300px', margin: '0 auto' }}>
              <div className="progress-fill" style={{ width: '60%' }}></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!extractionData) return null;

  return (
    <div>
      {/* Summary Stats */}
      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: '24px' }}>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: 'var(--accent-purple-dim)', color: 'var(--accent-purple)' }}>📋</div>
          <div className="stat-value">{extractionData.rules_extracted}</div>
          <div className="stat-label">Rules Extracted</div>
        </div>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: 'var(--accent-blue-dim)', color: 'var(--accent-blue)' }}>✅</div>
          <div className="stat-value">{extractionData.tasks_generated}</div>
          <div className="stat-label">MAPs Generated</div>
        </div>
        <div className="stat-card-lg">
          <div className="stat-icon" style={{ background: extractionData.conflicts_found > 0 ? 'var(--accent-red-dim)' : 'var(--accent-emerald-dim)', color: extractionData.conflicts_found > 0 ? 'var(--accent-red)' : 'var(--accent-emerald)' }}>
            {extractionData.conflicts_found > 0 ? '⚠️' : '✓'}
          </div>
          <div className="stat-value">{extractionData.conflicts_found}</div>
          <div className="stat-label">Conflicts Found</div>
        </div>
      </div>

      {/* Conflicts */}
      {extractionData.conflicts && extractionData.conflicts.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            ⚠️ Rule Conflicts Detected
          </h3>
          {extractionData.conflicts.map((conflict, i) => (
            <div key={i} className="conflict-alert">
              <div className="conflict-alert-header">
                <span className={`conflict-alert-type ${conflict.conflict_type?.toLowerCase()}`}>
                  {conflict.conflict_type}
                </span>
                <span className={`badge ${conflict.severity === 'High' ? 'badge-high' : 'badge-medium'}`}>
                  {conflict.severity}
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', marginBottom: '8px' }}>
                <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                  {conflict.new_rule_title}
                </span>
                <ArrowRight size={14} style={{ color: 'var(--text-tertiary)' }} />
                <span style={{ color: 'var(--accent-amber)' }}>
                  {conflict.existing_source}
                </span>
              </div>
              <div className="conflict-alert-reason">{conflict.reason}</div>
            </div>
          ))}
        </div>
      )}

      {/* Rules + Tasks Grid */}
      <div className="extraction-container">
        {/* Extracted Rules */}
        <div className="extraction-panel">
          <div className="extraction-panel-header">
            <Brain size={16} style={{ color: 'var(--accent-purple)' }} />
            Extracted Rules ({visibleRules.length}/{extractionData.rules?.length || 0})
          </div>
          <div className="extraction-panel-body">
            {visibleRules.map((rule, index) => (
              <div key={rule.rule_id || index} className="rule-card" style={{ animationDelay: `${index * 0.1}s` }}>
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
                  {rule.estimated_effort_days && (
                    <span className="badge" style={{ background: 'var(--bg-tertiary)', color: 'var(--text-tertiary)' }}>
                      ⏱ {rule.estimated_effort_days}d effort
                    </span>
                  )}
                </div>
                {rule.has_conflict && (
                  <div style={{ marginTop: '8px', padding: '6px 10px', background: 'rgba(248,113,113,0.08)', borderRadius: '6px', fontSize: '11px', color: 'var(--accent-red)' }}>
                    ⚠️ Conflict detected with existing rule
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Generated Tasks */}
        <div className="extraction-panel">
          <div className="extraction-panel-header">
            <Sparkles size={16} style={{ color: 'var(--accent-emerald)' }} />
            Generated MAPs ({visibleTasks.length}/{extractionData.tasks?.length || 0})
          </div>
          <div className="extraction-panel-body">
            {visibleTasks.map((task, index) => (
              <div key={task.task_ref || index} className="rule-card" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="rule-card-header">
                  <span className="rule-id">{task.task_ref}</span>
                  <StatusBadge status={task.status} />
                </div>
                <div className="rule-title" style={{ fontSize: '13px' }}>{task.title}</div>
                <div className="rule-meta" style={{ marginTop: '8px' }}>
                  <DepartmentBadge department={task.department} />
                  <PriorityBadge priority={task.priority} />
                  {task.deadline && (
                    <span className="badge" style={{ background: 'var(--bg-tertiary)', color: 'var(--text-tertiary)' }}>
                      📅 {task.deadline}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

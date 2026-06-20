import { Calendar, User, Building2, BookOpen } from 'lucide-react';
import StatusBadge, { PriorityBadge } from './StatusBadge';

export default function TaskCard({ task, onStatusFlip }) {
  const isFlipping = task._flipping;

  const flashClass = task._justVerified
    ? 'verified-flash'
    : task._justFailed
    ? 'failed-flash'
    : '';

  return (
    <div className={`task-card ${flashClass} ${isFlipping ? 'status-flip' : ''}`}>
      <div className="task-card-ref">{task.task_ref}</div>
      <div className="task-card-title">
        {task.title?.replace(/^\[.*?\]\s*/, '')}
      </div>
      <div className="task-card-footer">
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          <StatusBadge status={task.status} />
          <PriorityBadge priority={task.priority} />
        </div>
      </div>

      {/* Sub-vertical & Regulator info */}
      {(task.sub_vertical || task.regulator) && (
        <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
          {task.sub_vertical && (
            <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Building2 size={11} />
              {task.sub_vertical}
            </div>
          )}
          {task.regulator && (
            <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <BookOpen size={11} />
              {task.regulator}
              {task.advisory && <span style={{ opacity: 0.7 }}> — {task.advisory.length > 40 ? task.advisory.substring(0, 40) + '...' : task.advisory}</span>}
            </div>
          )}
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '10px' }}>
        {task.deadline && (
          <div className="task-card-deadline">
            <Calendar size={12} />
            {task.deadline}
          </div>
        )}
        {task.owner && (
          <div className="task-card-deadline">
            <User size={12} />
            {task.owner}
          </div>
        )}
      </div>

      {/* Routing reason tooltip */}
      {task.routing_reason && (
        <div style={{
          marginTop: '8px',
          padding: '6px 10px',
          background: 'var(--bg-tertiary)',
          borderRadius: '6px',
          fontSize: '10px',
          color: 'var(--text-tertiary)',
          lineHeight: '1.4'
        }}>
          🔄 {task.routing_reason.length > 120 ? task.routing_reason.substring(0, 120) + '...' : task.routing_reason}
        </div>
      )}

      {task.evidence_link && (
        <div style={{ marginTop: '8px', padding: '6px 10px', background: 'var(--accent-emerald-dim)', borderRadius: '6px', fontSize: '11px', color: 'var(--accent-emerald)' }}>
          📎 Evidence: {task.evidence_link}
        </div>
      )}
    </div>
  );
}

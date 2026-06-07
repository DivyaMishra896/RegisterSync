import { Calendar, User } from 'lucide-react';
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
      {task.evidence_link && (
        <div style={{ marginTop: '8px', padding: '6px 10px', background: 'var(--accent-emerald-dim)', borderRadius: '6px', fontSize: '11px', color: 'var(--accent-emerald)' }}>
          📎 Evidence: {task.evidence_link}
        </div>
      )}
    </div>
  );
}

export default function StatusBadge({ status }) {
  const statusMap = {
    'Pending': 'badge-pending',
    'Verified': 'badge-verified',
    'Failed': 'badge-failed',
    'Partially Done': 'badge-partial',
    'In Progress': 'badge-pending',
  };

  return (
    <span className={`badge ${statusMap[status] || 'badge-pending'}`}>
      {status === 'Verified' && '✓ '}
      {status === 'Failed' && '✕ '}
      {status === 'Partially Done' && '◐ '}
      {status}
    </span>
  );
}

export function PriorityBadge({ priority }) {
  const priorityMap = {
    'Critical': 'badge-critical',
    'High': 'badge-high',
    'Medium': 'badge-medium',
    'Low': 'badge-low',
  };

  return (
    <span className={`badge ${priorityMap[priority] || 'badge-medium'}`}>
      {priority}
    </span>
  );
}

export function DepartmentBadge({ department }) {
  const deptMap = {
    'IT Security': 'badge-dept-it',
    'Risk Management': 'badge-dept-risk',
    'Operations': 'badge-dept-ops',
  };

  return (
    <span className={`badge ${deptMap[department] || ''}`}>
      {department}
    </span>
  );
}

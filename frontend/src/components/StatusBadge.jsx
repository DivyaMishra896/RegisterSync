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

const DEPT_BADGE_MAP = {
  'Digital Banking Services': 'badge-dept-dbs',
  'Cybersecurity Wing': 'badge-dept-csw',
  'IT Vertical': 'badge-dept-itv',
  'Procurement & Vendor Management': 'badge-dept-pvm',
  'Credit Card Vertical': 'badge-dept-ccv',
  'Payments Vertical': 'badge-dept-pay',
  'Compliance Department': 'badge-dept-cmp',
  'Legal Department': 'badge-dept-leg',
  'Risk Management': 'badge-dept-rsk',
  'Internal Audit': 'badge-dept-aud',
};

export function DepartmentBadge({ department }) {
  const badgeClass = DEPT_BADGE_MAP[department] || '';

  return (
    <span className={`badge ${badgeClass}`}>
      {department}
    </span>
  );
}

import TaskCard from './TaskCard';
import {
  Monitor, AlertTriangle, Briefcase, Shield, CreditCard,
  Banknote, FileCheck, Scale, BarChart3, Search
} from 'lucide-react';

// 10 Business Verticals from Theme 2
const DEPT_CONFIG = {
  'Digital Banking Services': {
    icon: <Monitor size={16} />,
    color: 'var(--dept-dbs)',
    bgColor: 'var(--dept-dbs-dim)',
  },
  'Cybersecurity Wing': {
    icon: <Shield size={16} />,
    color: 'var(--dept-csw)',
    bgColor: 'var(--dept-csw-dim)',
  },
  'IT Vertical': {
    icon: <Monitor size={16} />,
    color: 'var(--dept-itv)',
    bgColor: 'var(--dept-itv-dim)',
  },
  'Procurement & Vendor Management': {
    icon: <Briefcase size={16} />,
    color: 'var(--dept-pvm)',
    bgColor: 'var(--dept-pvm-dim)',
  },
  'Credit Card Vertical': {
    icon: <CreditCard size={16} />,
    color: 'var(--dept-ccv)',
    bgColor: 'var(--dept-ccv-dim)',
  },
  'Payments Vertical': {
    icon: <Banknote size={16} />,
    color: 'var(--dept-pay)',
    bgColor: 'var(--dept-pay-dim)',
  },
  'Compliance Department': {
    icon: <FileCheck size={16} />,
    color: 'var(--dept-cmp)',
    bgColor: 'var(--dept-cmp-dim)',
  },
  'Legal Department': {
    icon: <Scale size={16} />,
    color: 'var(--dept-leg)',
    bgColor: 'var(--dept-leg-dim)',
  },
  'Risk Management': {
    icon: <AlertTriangle size={16} />,
    color: 'var(--dept-rsk)',
    bgColor: 'var(--dept-rsk-dim)',
  },
  'Internal Audit': {
    icon: <Search size={16} />,
    color: 'var(--dept-aud)',
    bgColor: 'var(--dept-aud-dim)',
  },
};

const ALL_DEPARTMENTS = Object.keys(DEPT_CONFIG);

export default function TaskBoard({ tasks }) {
  // Only show departments that have tasks assigned
  const activeDepartments = ALL_DEPARTMENTS.filter(
    dept => tasks.some(task => task.department === dept)
  );

  // If no active departments, show all departments
  const departments = activeDepartments.length > 0 ? activeDepartments : ALL_DEPARTMENTS;

  const getTasksByDepartment = (dept) =>
    tasks.filter(task => task.department === dept);

  return (
    <div className="task-board">
      {departments.map(dept => {
        const deptTasks = getTasksByDepartment(dept);
        const config = DEPT_CONFIG[dept] || {
          icon: <Briefcase size={16} />,
          color: 'var(--text-secondary)',
          bgColor: 'var(--bg-tertiary)',
        };

        return (
          <div key={dept} className="task-column">
            <div className="task-column-header">
              <div className="task-column-title" style={{ color: config.color }}>
                <span style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: 'var(--radius-sm)',
                  background: config.bgColor,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: config.color,
                }}>
                  {config.icon}
                </span>
                <span style={{ fontSize: '12px' }}>{dept}</span>
              </div>
              <span className="task-column-count">{deptTasks.length}</span>
            </div>
            <div className="task-column-body">
              {deptTasks.length === 0 ? (
                <div className="empty-state" style={{ padding: '30px 10px' }}>
                  <div className="empty-state-text">No tasks assigned</div>
                </div>
              ) : (
                deptTasks.map(task => (
                  <TaskCard key={task.id || task.task_ref} task={task} />
                ))
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

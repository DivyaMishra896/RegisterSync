import TaskCard from './TaskCard';
import { Monitor, AlertTriangle, Briefcase } from 'lucide-react';

const DEPT_CONFIG = {
  'IT Security': {
    icon: <Monitor size={16} />,
    color: 'var(--dept-it)',
    bgColor: 'var(--dept-it-dim)',
  },
  'Risk Management': {
    icon: <AlertTriangle size={16} />,
    color: 'var(--dept-risk)',
    bgColor: 'var(--dept-risk-dim)',
  },
  'Operations': {
    icon: <Briefcase size={16} />,
    color: 'var(--dept-ops)',
    bgColor: 'var(--dept-ops-dim)',
  },
};

export default function TaskBoard({ tasks }) {
  const departments = ['IT Security', 'Risk Management', 'Operations'];

  const getTasksByDepartment = (dept) =>
    tasks.filter(task => task.department === dept);

  return (
    <div className="task-board">
      {departments.map(dept => {
        const deptTasks = getTasksByDepartment(dept);
        const config = DEPT_CONFIG[dept];

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
                {dept}
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

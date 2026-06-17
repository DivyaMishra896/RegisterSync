import { useState, useEffect } from 'react';
import { LayoutDashboard, RefreshCw, TrendingUp, Clock, CheckCircle, XCircle, Shield, AlertTriangle } from 'lucide-react';
import TaskBoard from '../components/TaskBoard';
import VerificationPanel from '../components/VerificationPanel';
import ImpactPredictor from '../components/ImpactPredictor';
import { getTasks, getTaskStats } from '../api/client';

export default function DashboardPage() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState('all');
  const [showCharts, setShowCharts] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [tasksRes, statsRes] = await Promise.all([
        getTasks(),
        getTaskStats(),
      ]);
      setTasks(tasksRes.data.tasks || []);
      setStats(statsRes.data);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleVerificationComplete = async (results) => {
    // Refresh tasks to show status updates
    await fetchData();

    // Add flash animations to updated tasks
    if (results?.details) {
      setTasks(prev => prev.map(task => {
        const detail = results.details.find(d => d.task_ref === task.task_ref);
        if (detail && detail.new_status !== detail.previous_status) {
          return {
            ...task,
            _justVerified: detail.new_status === 'Verified',
            _justFailed: detail.new_status === 'Failed',
            _flipping: true,
          };
        }
        return task;
      }));

      // Clear animations after 2 seconds
      setTimeout(() => {
        setTasks(prev => prev.map(task => ({
          ...task,
          _justVerified: false,
          _justFailed: false,
          _flipping: false,
        })));
      }, 2000);
    }
  };

  const filteredTasks = activeFilter === 'all'
    ? tasks
    : tasks.filter(t => t.status === activeFilter);

  if (loading) {
    return (
      <div className="page-enter">
        <div className="page-header">
          <div className="page-title">
            <LayoutDashboard size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
            Compliance Dashboard
          </div>
        </div>
        <div className="page-content">
          <div className="stats-grid">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="stat-card-lg">
                <div className="skeleton" style={{ width: '40px', height: '40px', marginBottom: '12px' }}></div>
                <div className="skeleton" style={{ width: '60px', height: '32px', marginBottom: '8px' }}></div>
                <div className="skeleton" style={{ width: '100px', height: '14px' }}></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="page-enter">
        <div className="page-header">
          <div className="page-title">
            <LayoutDashboard size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
            Compliance Dashboard
          </div>
          <div className="page-subtitle">Monitor and verify regulatory compliance tasks</div>
        </div>
        <div className="page-content">
          <div className="empty-state">
            <div className="empty-state-icon">📋</div>
            <div className="empty-state-title">No tasks yet</div>
            <div className="empty-state-text">
              Upload a regulatory circular first. Go to the Upload page to get started.
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-enter">
      <div className="page-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div className="page-title">
            <LayoutDashboard size={20} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
            Compliance Dashboard
          </div>
          <div className="page-subtitle">Monitor and verify regulatory compliance tasks</div>
        </div>
        <button className="btn btn-outline btn-sm" onClick={fetchData}>
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      <div className="page-content">
        {/* Stats Overview */}
        <div className="stats-grid">
          <div className="stat-card-lg">
            <div className="stat-icon" style={{ background: 'var(--accent-purple-dim)', color: 'var(--accent-purple)' }}>
              <TrendingUp size={18} />
            </div>
            <div className="stat-value">{stats?.total || 0}</div>
            <div className="stat-label">Total Tasks</div>
          </div>

          <div className="stat-card-lg">
            <div className="stat-icon" style={{ background: 'var(--accent-emerald-dim)', color: 'var(--accent-emerald)' }}>
              <CheckCircle size={18} />
            </div>
            <div className="stat-value" style={{ color: 'var(--accent-emerald)' }}>
              {stats?.by_status?.Verified || 0}
            </div>
            <div className="stat-label">Verified</div>
          </div>

          <div className="stat-card-lg">
            <div className="stat-icon" style={{ background: 'var(--status-pending-dim)', color: 'var(--status-pending)' }}>
              <Clock size={18} />
            </div>
            <div className="stat-value" style={{ color: 'var(--status-pending)' }}>
              {stats?.by_status?.Pending || 0}
            </div>
            <div className="stat-label">Pending</div>
          </div>

          <div className="stat-card-lg" style={{ background: stats?.risk_level?.includes('CRITICAL') || stats?.risk_level?.includes('HIGH') ? 'rgba(248, 113, 113, 0.05)' : 'var(--bg-secondary)' }}>
            <div className="stat-icon" style={{ 
              background: stats?.risk_score < 75 ? 'var(--accent-red-dim)' : 'var(--accent-emerald-dim)', 
              color: stats?.risk_score < 75 ? 'var(--accent-red)' : 'var(--accent-emerald)' 
            }}>
              <AlertTriangle size={18} />
            </div>
            <div className="gauge-container" style={{ padding: '0' }}>
              <div className="stat-value" style={{ 
                fontSize: '28px',
                color: stats?.risk_score < 75 ? 'var(--accent-red)' : 'var(--accent-emerald)'
              }}>
                <span className="gauge-value" style={{ fontSize: '28px' }}>
                  {stats?.risk_score || 0}/100
                </span>
              </div>
            </div>
            <div className="stat-label">
              {stats?.risk_level || 'Calculating...'}
            </div>
          </div>
        </div>

        {/* Filter Bar */}
        <div className="filter-bar">
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)', marginRight: '4px' }}>Filter:</span>
          {['all', 'Pending', 'Verified', 'Failed', 'Partially Done'].map(filter => (
            <button
              key={filter}
              className={`filter-chip ${activeFilter === filter ? 'active' : ''}`}
              onClick={() => setActiveFilter(filter)}
            >
              {filter === 'all' ? 'All Tasks' : filter}
              {filter !== 'all' && stats?.by_status?.[filter] !== undefined && (
                <span style={{ marginLeft: '4px', opacity: 0.7 }}>({stats.by_status[filter]})</span>
              )}
            </button>
          ))}

          <div style={{ marginLeft: 'auto' }}>
            <button
              className={`filter-chip ${showCharts ? 'active' : ''}`}
              onClick={() => setShowCharts(!showCharts)}
            >
              📊 Charts
            </button>
          </div>
        </div>

        {/* Task Board */}
        <TaskBoard tasks={filteredTasks} />

        {/* Impact Charts */}
        {showCharts && (
          <div style={{ marginTop: '28px' }}>
            <ImpactPredictor stats={stats} tasks={tasks} />
          </div>
        )}

        {/* Verification Agent */}
        <VerificationPanel onVerificationComplete={handleVerificationComplete} />
      </div>
    </div>
  );
}

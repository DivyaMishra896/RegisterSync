import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const DEPT_COLORS = {
  'IT Security': '#60a5fa',
  'Risk Management': '#fbbf24',
  'Operations': '#34d399',
};

const STATUS_COLORS = {
  'Pending': '#fbbf24',
  'Verified': '#34d399',
  'Failed': '#f87171',
  'Partially Done': '#fb923c',
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div style={{
      background: 'rgba(255, 255, 255, 0.95)',
      border: '1px solid rgba(0,0,0,0.1)',
      borderRadius: '8px',
      padding: '10px 14px',
      backdropFilter: 'blur(10px)',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)'
    }}>
      <div style={{ fontSize: '12px', fontWeight: 600, color: '#000000', marginBottom: '4px' }}>{label}</div>
      {payload.map((entry, i) => (
        <div key={i} style={{ fontSize: '11px', color: '#4b4b5e', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: entry.color }}></span>
          {entry.name}: <span style={{ fontWeight: 600, color: '#000000' }}>{entry.value}</span> {entry.name === 'Effort' ? 'days' : 'tasks'}
        </div>
      ))}
    </div>
  );
};

export default function ImpactPredictor({ stats, tasks }) {
  if (!stats || !tasks || tasks.length === 0) {
    return (
      <div className="chart-container">
        <div className="chart-title">📊 Impact Predictor</div>
        <div className="empty-state">
          <div className="empty-state-text">No data available yet. Upload and extract a circular first.</div>
        </div>
      </div>
    );
  }

  // Effort by department data
  const effortData = Object.entries(stats.effort_by_department || {}).map(([dept, effort]) => ({
    department: dept,
    Effort: effort,
    fill: DEPT_COLORS[dept] || '#6b7280',
  }));

  // Tasks by department
  const taskCountData = Object.entries(stats.by_department || {}).map(([dept, data]) => ({
    department: dept,
    Total: data.total,
    Verified: data.verified,
    Pending: data.pending,
    Failed: data.failed,
  }));

  // Status distribution for pie chart
  const statusData = Object.entries(stats.by_status || {}).map(([status, count]) => ({
    name: status,
    value: count,
    color: STATUS_COLORS[status] || '#6b7280',
  }));

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      {/* Effort by Department */}
      <div className="chart-container">
        <div className="chart-title">⏱ Estimated Effort by Department</div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={effortData} margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" />
            <XAxis
              dataKey="department"
              tick={{ fill: '#8b8b9e', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#8b8b9e', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              tickLine={false}
              label={{ value: 'Days', angle: -90, position: 'insideLeft', fill: '#5a5a6e', fontSize: 11 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Effort" radius={[4, 4, 0, 0]}>
              {effortData.map((entry, index) => (
                <Cell key={index} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Status Distribution */}
      <div className="chart-container">
        <div className="chart-title">📈 Compliance Status</div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={90}
                paddingAngle={4}
                dataKey="value"
                stroke="none"
              >
                {statusData.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend
                verticalAlign="bottom"
                iconType="circle"
                iconSize={8}
                formatter={(value) => <span style={{ color: '#8b8b9e', fontSize: '11px' }}>{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Task Count by Department */}
      <div className="chart-container" style={{ gridColumn: 'span 2' }}>
        <div className="chart-title">🏢 Tasks by Department & Status</div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={taskCountData} margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" />
            <XAxis
              dataKey="department"
              tick={{ fill: '#8b8b9e', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#8b8b9e', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              iconType="circle"
              iconSize={8}
              formatter={(value) => <span style={{ color: '#8b8b9e', fontSize: '11px' }}>{value}</span>}
            />
            <Bar dataKey="Verified" fill="#34d399" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Pending" fill="#fbbf24" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Failed" fill="#f87171" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

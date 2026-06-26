import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const DEPT_COLORS = {
  'Digital Banking Services': '#3b82f6',
  'Cybersecurity Wing': '#c62828',
  'IT Vertical': '#6d4aab',
  'Procurement & Vendor Management': '#d97706',
  'Credit Card Vertical': '#c2185b',
  'Payments Vertical': '#0284c7',
  'Compliance Department': '#107c10',
  'Legal Department': '#e65100',
  'Risk Management': '#f9a825',
  'Internal Audit': '#4a52c9',
};

const STATUS_COLORS = {
  'Pending': '#d97706',
  'Verified': '#107c10',
  'Failed': '#c62828',
  'Partially Done': '#e65100',
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div style={{
      background: '#FFFFFF',
      border: '1px solid #E8E4DF',
      borderRadius: '8px',
      padding: '12px 16px',
      boxShadow: '0 4px 12px rgba(26, 26, 26, 0.06)',
    }}>
      <div style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: '13px', fontWeight: 600, color: '#1A1A1A', marginBottom: '6px' }}>{label}</div>
      {payload.map((entry, i) => (
        <div key={i} style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: '11px', color: '#5A5A5A', display: 'flex', alignItems: 'center', gap: '6px', marginTop: '2px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: entry.color }}></span>
          {entry.name}: <span style={{ fontWeight: 600, color: '#1A1A1A' }}>{entry.value}</span> {entry.name === 'Effort' ? 'days' : 'tasks'}
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

  const effortData = Object.entries(stats.effort_by_department || {}).map(([dept, effort]) => ({
    department: dept,
    Effort: effort,
    fill: DEPT_COLORS[dept] || '#8A8A8A',
  }));

  const taskCountData = Object.entries(stats.by_department || {}).map(([dept, data]) => ({
    department: dept,
    Total: data.total,
    Verified: data.verified,
    Pending: data.pending,
    Failed: data.failed,
  }));

  const statusData = Object.entries(stats.by_status || {}).map(([status, count]) => ({
    name: status,
    value: count,
    color: STATUS_COLORS[status] || '#8A8A8A',
  }));

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <div className="chart-container">
        <div className="chart-title">⏱ Estimated Effort by Department</div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={effortData} margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E8E4DF" />
            <XAxis
              dataKey="department"
              tick={{ fill: '#8A8A8A', fontSize: 10, fontFamily: "'IBM Plex Mono', monospace" }}
              axisLine={{ stroke: '#E8E4DF' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#8A8A8A', fontSize: 10, fontFamily: "'IBM Plex Mono', monospace" }}
              axisLine={{ stroke: '#E8E4DF' }}
              tickLine={false}
              label={{ value: 'Days', angle: -90, position: 'insideLeft', fill: '#5A5A5A', fontSize: 11, fontFamily: "'IBM Plex Mono', monospace" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="Effort" radius={[3, 3, 0, 0]}>
              {effortData.map((entry, index) => (
                <Cell key={index} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

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
                iconSize={7}
                formatter={(value) => <span style={{ color: '#8A8A8A', fontSize: '10px', fontFamily: "'IBM Plex Mono', monospace", letterSpacing: '0.06em', textTransform: 'uppercase' }}>{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="chart-container" style={{ gridColumn: 'span 2' }}>
        <div className="chart-title">🏢 Tasks by Department & Status</div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={taskCountData} margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E8E4DF" />
            <XAxis
              dataKey="department"
              tick={{ fill: '#8A8A8A', fontSize: 10, fontFamily: "'IBM Plex Mono', monospace" }}
              axisLine={{ stroke: '#E8E4DF' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#8A8A8A', fontSize: 10, fontFamily: "'IBM Plex Mono', monospace" }}
              axisLine={{ stroke: '#E8E4DF' }}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              iconType="circle"
              iconSize={7}
              formatter={(value) => <span style={{ color: '#8A8A8A', fontSize: '10px', fontFamily: "'IBM Plex Mono', monospace", letterSpacing: '0.06em', textTransform: 'uppercase' }}>{value}</span>}
            />
            <Bar dataKey="Verified" fill="#107c10" radius={[3, 3, 0, 0]} />
            <Bar dataKey="Pending" fill="#d97706" radius={[3, 3, 0, 0]} />
            <Bar dataKey="Failed" fill="#c62828" radius={[3, 3, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

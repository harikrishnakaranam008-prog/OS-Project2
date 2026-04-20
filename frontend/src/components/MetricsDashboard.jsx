import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function MetricsDashboard({ result }) {
  if (!result) return null;

  return (
    <div className="metrics-grid">
      <div className="metric-card">
        <div className="metric-label">Avg Waiting Time</div>
        <div className="metric-value">{result.avg_waiting_time.toFixed(2)}ms</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Avg Turnaround</div>
        <div className="metric-value">{result.avg_turnaround_time.toFixed(2)}ms</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Avg Response</div>
        <div className="metric-value">{result.avg_response_time.toFixed(2)}ms</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">CPU Utilization</div>
        <div className="metric-value">{result.cpu_utilization.toFixed(1)}%</div>
      </div>
    </div>
  );
}

MetricsDashboard.ComparisonChart = function ComparisonChart({ results }) {
  if (!results) return null;

  const data = results.map(r => ({
    name: r.algorithm.replace(' Scheduler', ''),
    waiting: r.avg_waiting_time,
    turnaround: r.avg_turnaround_time,
  }));

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis dataKey="name" stroke="var(--text-muted)" tick={{fontSize: 12}} />
          <YAxis stroke="var(--text-muted)" tick={{fontSize: 12}} />
          <Tooltip 
            contentStyle={{ backgroundColor: 'var(--panel-bg)', borderColor: 'var(--border)', borderRadius: '8px' }}
            itemStyle={{ color: 'var(--text-color)' }}
          />
          <Legend />
          <Bar dataKey="waiting" name="Waiting Time" fill="var(--primary)" radius={[4, 4, 0, 0]} />
          <Bar dataKey="turnaround" name="Turnaround Time" fill="var(--accent)" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

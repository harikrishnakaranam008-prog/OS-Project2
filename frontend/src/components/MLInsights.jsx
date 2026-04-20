import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export default function MLInsights({ result }) {
  if (!result || !result.processes) return <p>No ML data available</p>;

  const data = result.processes.map(p => ({
    name: p.pid,
    actual: p.burst_time,
    predicted: p.predicted_burst_time !== null ? Number(p.predicted_burst_time.toFixed(1)) : p.burst_time,
    error: Math.abs(p.burst_time - (p.predicted_burst_time || p.burst_time))
  }));

  const avgError = data.reduce((acc, curr) => acc + curr.error, 0) / data.length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ width: '100%', height: 250 }}>
        <ResponsiveContainer>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis type="number" dataKey="actual" name="Actual Burst" label={{ value: 'Actual Time', position: 'insideBottom', offset: -10, fill: 'var(--text-muted)' }} stroke="var(--text-muted)" />
            <YAxis type="number" dataKey="predicted" name="Predicted Burst" label={{ value: 'Predicted Time', angle: -90, position: 'insideLeft', fill: 'var(--text-muted)' }} stroke="var(--text-muted)" />
            <Tooltip
              cursor={{ strokeDasharray: '3 3' }}
              contentStyle={{ backgroundColor: 'var(--panel-bg)', borderColor: 'var(--border)', borderRadius: '8px' }}
            />
            {/* y=x reference line for perfect predictions */}
            <ReferenceLine x={0} y={0} stroke="white" />
            <Scatter name="Processes" data={data} fill="var(--success)" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Mean Absolute Error (Simulation)</span>
          <span style={{ fontWeight: 600, color: 'var(--warning)' }}>{avgError.toFixed(2)} ms</span>
        </div>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
          The ML Hybrid scheduler leverages these predictions to optimize Shortest Job First ordering dynamically.
        </p>
      </div>
    </div>
  );
}

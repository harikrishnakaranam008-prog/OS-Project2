import React, { useEffect, useState } from 'react';

const colors = [
  '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', 
  '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16'
];

export default function GanttChart({ result }) {
  const [animatedChart, setAnimatedChart] = useState([]);
  
  useEffect(() => {
    if (!result || !result.gantt_chart) return;
    
    // Animate the blocks
    setAnimatedChart([]);
    let timer;
    
    const animate = () => {
      result.gantt_chart.forEach((block, index) => {
        timer = setTimeout(() => {
          setAnimatedChart(prev => [...prev, block]);
        }, index * 200); // 200ms per block
      });
    };
    
    animate();
    
    return () => clearTimeout(timer);
  }, [result]);

  if (!result || !result.gantt_chart) return null;

  const totalTime = Math.max(...result.gantt_chart.map(b => b.end), 1);

  return (
    <div className="gantt-container">
      <div className="gantt-track">
        {animatedChart.map((block, i) => {
          const width = ((block.end - block.start) / totalTime) * 100;
          const pidNum = parseInt(block.pid.replace('P', ''));
          const bgColor = colors[(pidNum - 1) % colors.length];
          
          return (
            <div 
              key={`${block.pid}-${i}`}
              className="gantt-block"
              style={{
                width: `${width}%`,
                backgroundColor: bgColor,
              }}
              data-tooltip={`${block.pid} (${block.start} - ${block.end})`}
            >
              {width > 3 ? block.pid : ''}
            </div>
          );
        })}
      </div>
      
      {/* Timeline markers */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
        <span>0</span>
        <span>{totalTime}</span>
      </div>
    </div>
  );
}

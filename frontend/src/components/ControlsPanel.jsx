import React, { useState } from 'react';
import { Settings, Play, Square, RotateCcw } from 'lucide-react';

export default function ControlsPanel({ onSimulate, loading }) {
  const [params, setParams] = useState({
    numProcesses: 5,
    timeQuantum: 4,
    workloadType: 'mixed'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParams(prev => ({ ...prev, [name]: name === 'workloadType' ? value : Number(value) }));
  };

  return (
    <div className="glass-panel">
      <h2 className="panel-title"><Settings size={20} /> Simulation Controls</h2>
      
      <div className="control-group">
        <label>Number of Processes: {params.numProcesses}</label>
        <input 
          type="range" 
          name="numProcesses" 
          min="3" max="15" 
          value={params.numProcesses} 
          onChange={handleChange} 
          className="control-input"
          style={{padding: 0}}
        />
      </div>

      <div className="control-group">
        <label>Time Quantum (RR): {params.timeQuantum}</label>
        <input 
          type="range" 
          name="timeQuantum" 
          min="1" max="10" 
          value={params.timeQuantum} 
          onChange={handleChange} 
          className="control-input"
          style={{padding: 0}}
        />
      </div>

      <div className="control-group">
        <label>Workload Type</label>
        <select 
          name="workloadType" 
          value={params.workloadType} 
          onChange={handleChange}
          className="control-input"
        >
          <option value="mixed">Mixed (Realistic)</option>
          <option value="cpu">CPU Bound Heavy</option>
          <option value="io">I/O Bound Heavy</option>
        </select>
      </div>

      <div className="btn-group">
        <button 
          className="btn btn-primary" 
          onClick={() => onSimulate(params)}
          disabled={loading}
        >
          {loading ? 'Simulating...' : <><Play size={18} /> Start</>}
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => onSimulate(params)}
        >
          <RotateCcw size={18} /> Reset
        </button>
      </div>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import ControlsPanel from './components/ControlsPanel';
import GanttChart from './components/GanttChart';
import MetricsDashboard from './components/MetricsDashboard';
import MLInsights from './components/MLInsights';
import { Cpu, Activity, Brain } from 'lucide-react';

function App() {
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedAlgo, setSelectedAlgo] = useState('ML Hybrid Scheduler');

  const runSimulation = async (params) => {
    setLoading(true);
    try {
      // Generate processes based on params
      const processes = [];
      let currentTime = 0;
      
      for (let i = 0; i < params.numProcesses; i++) {
        const type = params.workloadType === 'mixed' ? Math.floor(Math.random() * 3) 
                   : params.workloadType === 'cpu' ? 0 : 1;
                   
        let burst = type === 0 ? Math.floor(Math.random() * 15) + 5 
                  : Math.floor(Math.random() * 5) + 1;
                  
        processes.push({
          pid: `P${i+1}`,
          arrival_time: currentTime,
          burst_time: burst,
          priority: Math.floor(Math.random() * 5) + 1,
          process_type: type,
          prev_burst_time: Math.floor(Math.max(1, burst + (Math.random() * 4 - 2)))
        });
        
        currentTime += Math.floor(Math.random() * 3);
      }

      const response = await fetch('http://localhost:8000/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          processes,
          time_quantum: params.timeQuantum
        })
      });
      
      const data = await response.json();
      setSimulationData(data.results);
    } catch (error) {
      console.error("Simulation failed", error);
    } finally {
      setLoading(false);
    }
  };

  const currentResult = simulationData?.find(r => r.algorithm === selectedAlgo);

  return (
    <div className="app-container">
      <header>
        <h1>Intelligent OS Scheduler</h1>
        <p>Machine Learning powered CPU scheduling optimization</p>
      </header>
      
      <div className="dashboard-grid">
        <aside>
          <ControlsPanel onSimulate={runSimulation} loading={loading} />
          
          {simulationData && (
            <div className="glass-panel" style={{marginTop: '1.5rem'}}>
              <h2 className="panel-title"><Activity size={20} /> Algorithms</h2>
              <select 
                className="control-input"
                value={selectedAlgo}
                onChange={e => setSelectedAlgo(e.target.value)}
              >
                {simulationData.map(r => (
                  <option key={r.algorithm} value={r.algorithm}>{r.algorithm}</option>
                ))}
              </select>
            </div>
          )}
        </aside>
        
        <main className="main-content">
          {simulationData ? (
            <>
              <div className="glass-panel">
                <h2 className="panel-title"><Cpu size={20} /> CPU Timeline ({currentResult?.algorithm})</h2>
                <GanttChart result={currentResult} />
              </div>
              
              <div className="glass-panel">
                <h2 className="panel-title"><Activity size={20} /> Performance Metrics</h2>
                <MetricsDashboard result={currentResult} allResults={simulationData} />
              </div>
              
              <div className="charts-row">
                <div className="glass-panel">
                  <h2 className="panel-title"><Brain size={20} /> ML Prediction Insights</h2>
                  <MLInsights result={simulationData.find(r => r.algorithm === 'ML Hybrid Scheduler')} />
                </div>
                <div className="glass-panel">
                  <h2 className="panel-title">Algorithm Comparison</h2>
                  <MetricsDashboard.ComparisonChart results={simulationData} />
                </div>
              </div>
            </>
          ) : (
            <div className="glass-panel" style={{display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px', flexDirection: 'column', gap: '1rem', color: 'var(--text-muted)'}}>
              <Cpu size={48} opacity={0.5} />
              <p>Configure parameters and start simulation</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;

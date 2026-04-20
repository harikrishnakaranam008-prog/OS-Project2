from .models import Process, SimulationResult
from .algorithms import calculate_metrics
import copy

def ml_hybrid_scheduler(processes_in: list[Process], quantum: int = 4):
    """
    ML Hybrid Scheduler uses predicted burst times.
    It combines SJF (Shortest Job First based on prediction) and Round Robin to avoid starvation.
    It operates dynamically.
    """
    processes = copy.deepcopy(processes_in)
    n = len(processes)
    gantt_chart = []
    current_time = 0
    completed = 0
    
    for p in processes:
        p.remaining_time = p.burst_time # Actual execution still depends on true burst
        # If prediction fails, fallback to actual
        p.predicted_burst_time = p.predicted_burst_time if p.predicted_burst_time is not None else p.burst_time
        
    processes.sort(key=lambda x: x.arrival_time)
    
    idx = 0
    if processes:
        current_time = processes[0].arrival_time
        
    ready_queue = []
    
    while completed != n:
        while idx < n and processes[idx].arrival_time <= current_time:
            ready_queue.append(processes[idx])
            idx += 1
            
        if not ready_queue:
            current_time += 1
            continue
            
        # Core logic of ML Scheduler: 
        # Sort ready queue based on predicted remaining time to prioritize short jobs (SRTF flavor).
        # We also consider priority to some extent.
        # Scoring: w1 * predicted_burst + w2 * priority
        ready_queue.sort(key=lambda x: (x.predicted_burst_time, x.priority))
        
        p = ready_queue.pop(0)
        
        if p.response_time == -1:
            p.response_time = current_time
            
        start = current_time
        
        # Determine execution slice. If predicted burst is very small, we might let it finish.
        # Otherwise, we use an adaptive quantum based on the prediction.
        adaptive_quantum = max(2, int(p.predicted_burst_time * 0.5)) if p.predicted_burst_time > quantum else quantum
        execution_time = min(adaptive_quantum, p.remaining_time)
        
        current_time += execution_time
        p.remaining_time -= execution_time
        # Reduce the predicted remaining burst time 
        p.predicted_burst_time = max(0, p.predicted_burst_time - execution_time)
        
        if not gantt_chart or gantt_chart[-1]["pid"] != p.pid:
            gantt_chart.append({"pid": p.pid, "start": start, "end": current_time})
        else:
            gantt_chart[-1]["end"] = current_time
            
        while idx < n and processes[idx].arrival_time <= current_time:
            ready_queue.append(processes[idx])
            idx += 1
            
        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            completed += 1
            
    return calculate_metrics(processes, gantt_chart, "ML Hybrid Scheduler")

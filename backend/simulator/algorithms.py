from .models import Process, SimulationResult
import copy

def calculate_metrics(processes, gantt_chart, algorithm):
    n = len(processes)
    if n == 0:
        return SimulationResult(algorithm=algorithm, processes=[], gantt_chart=[], avg_waiting_time=0, avg_turnaround_time=0, avg_response_time=0, cpu_utilization=0, throughput=0)
    
    total_waiting = 0
    total_turnaround = 0
    total_response = 0
    
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += (p.response_time - p.arrival_time)
        
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n
    avg_response = total_response / n
    
    total_time = max([p.completion_time for p in processes]) if processes else 0
    idle_time = 0
    
    # Calculate idle time from gantt chart
    if gantt_chart:
        idle_time += gantt_chart[0]['start']
        for i in range(1, len(gantt_chart)):
            idle_time += max(0, gantt_chart[i]['start'] - gantt_chart[i-1]['end'])
            
    cpu_utilization = ((total_time - idle_time) / total_time * 100) if total_time > 0 else 0
    throughput = n / total_time if total_time > 0 else 0
    
    return SimulationResult(
        algorithm=algorithm,
        processes=processes,
        gantt_chart=gantt_chart,
        avg_waiting_time=avg_waiting,
        avg_turnaround_time=avg_turnaround,
        avg_response_time=avg_response,
        cpu_utilization=cpu_utilization,
        throughput=throughput
    )

def fcfs(processes_in: list[Process]):
    processes = copy.deepcopy(processes_in)
    processes.sort(key=lambda x: x.arrival_time)
    
    gantt_chart = []
    current_time = 0
    
    for p in processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        
        start = current_time
        p.response_time = start
        
        current_time += p.burst_time
        p.completion_time = current_time
        
        gantt_chart.append({"pid": p.pid, "start": start, "end": current_time})
        
    return calculate_metrics(processes, gantt_chart, "FCFS")

def sjf(processes_in: list[Process]): # Non-preemptive
    processes = copy.deepcopy(processes_in)
    n = len(processes)
    gantt_chart = []
    current_time = 0
    completed = 0
    
    ready_queue = []
    
    while completed != n:
        # add to ready queue
        for p in processes:
            if p.arrival_time <= current_time and p not in ready_queue and p.completion_time == 0:
                ready_queue.append(p)
                
        if not ready_queue:
            current_time += 1
            continue
            
        # sort by burst time
        ready_queue.sort(key=lambda x: x.burst_time)
        p = ready_queue.pop(0)
        
        start = current_time
        if p.response_time == -1:
            p.response_time = start
            
        current_time += p.burst_time
        p.completion_time = current_time
        completed += 1
        
        gantt_chart.append({"pid": p.pid, "start": start, "end": current_time})
        
    return calculate_metrics(processes, gantt_chart, "SJF")

def round_robin(processes_in: list[Process], quantum: int = 4):
    processes = copy.deepcopy(processes_in)
    n = len(processes)
    gantt_chart = []
    current_time = 0
    completed = 0
    
    ready_queue = []
    for p in processes:
        p.remaining_time = p.burst_time
        
    processes.sort(key=lambda x: x.arrival_time)
    
    idx = 0
    if processes:
        current_time = processes[0].arrival_time
        
    while completed != n:
        while idx < n and processes[idx].arrival_time <= current_time:
            ready_queue.append(processes[idx])
            idx += 1
            
        if not ready_queue:
            current_time += 1
            continue
            
        p = ready_queue.pop(0)
        
        if p.response_time == -1:
            p.response_time = current_time
            
        start = current_time
        execution_time = min(quantum, p.remaining_time)
        
        current_time += execution_time
        p.remaining_time -= execution_time
        
        gantt_chart.append({"pid": p.pid, "start": start, "end": current_time})
        
        # Check for new arrivals while this process was executing
        while idx < n and processes[idx].arrival_time <= current_time:
            ready_queue.append(processes[idx])
            idx += 1
            
        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            completed += 1
            
    # Merge consecutive gantt chart blocks for same PID if they exist
    merged_gantt = []
    for block in gantt_chart:
        if merged_gantt and merged_gantt[-1]["pid"] == block["pid"]:
            merged_gantt[-1]["end"] = block["end"]
        else:
            merged_gantt.append(block)
            
    return calculate_metrics(processes, merged_gantt, "Round Robin")

def priority_scheduling(processes_in: list[Process]): # Preemptive Priority (Lower number = higher priority)
    processes = copy.deepcopy(processes_in)
    n = len(processes)
    gantt_chart = []
    current_time = 0
    completed = 0
    
    for p in processes:
        p.remaining_time = p.burst_time
        
    while completed != n:
        ready_queue = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not ready_queue:
            current_time += 1
            continue
            
        # sort by priority (lowest value first), then arrival time
        ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
        p = ready_queue[0]
        
        if p.response_time == -1:
            p.response_time = current_time
            
        start = current_time
        current_time += 1
        p.remaining_time -= 1
        
        if not gantt_chart or gantt_chart[-1]["pid"] != p.pid:
            gantt_chart.append({"pid": p.pid, "start": start, "end": current_time})
        else:
            gantt_chart[-1]["end"] = current_time
            
        if p.remaining_time == 0:
            p.completion_time = current_time
            completed += 1
            
    return calculate_metrics(processes, gantt_chart, "Priority")

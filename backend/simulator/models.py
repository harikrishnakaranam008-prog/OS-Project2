from pydantic import BaseModel
from typing import List, Optional

class Process(BaseModel):
    pid: str
    arrival_time: int
    burst_time: int
    priority: int
    process_type: int # 0: CPU-bound, 1: I/O-bound, 2: Mixed
    prev_burst_time: int = 5
    predicted_burst_time: Optional[float] = None
    
    # Simulation state
    remaining_time: Optional[int] = None
    start_time: Optional[int] = -1
    completion_time: Optional[int] = 0
    waiting_time: Optional[int] = 0
    turnaround_time: Optional[int] = 0
    response_time: Optional[int] = -1

    def __init__(self, **data):
        super().__init__(**data)
        if self.remaining_time is None:
            self.remaining_time = self.burst_time

class SimulationResult(BaseModel):
    algorithm: str
    processes: List[Process]
    gantt_chart: List[dict] # list of {"pid": str, "start": int, "end": int}
    avg_waiting_time: float
    avg_turnaround_time: float
    avg_response_time: float
    cpu_utilization: float
    throughput: float

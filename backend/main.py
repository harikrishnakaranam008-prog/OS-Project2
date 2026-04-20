from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pickle
import numpy as np
import pandas as pd
import os
import time

from simulator.models import Process, SimulationResult
from simulator.algorithms import fcfs, sjf, round_robin, priority_scheduling
from simulator.ml_scheduler import ml_hybrid_scheduler

app = FastAPI(title="Intelligent CPU Scheduler API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "../ml_model/model.pkl"
ml_model = None

@app.on_event("startup")
async def load_model():
    global ml_model
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                ml_model = pickle.load(f)
            print("ML model loaded successfully.")
        else:
            print(f"Model not found at {MODEL_PATH}. Predictions will be random or defaults.")
    except Exception as e:
        print(f"Error loading model: {e}")

class SimulationRequest(BaseModel):
    processes: List[dict]
    time_quantum: int = 4

@app.post("/api/simulate")
async def run_simulation(req: SimulationRequest):
    process_list = []
    
    # Process inputs and make ML predictions if model is available
    for p_data in req.processes:
        process = Process(**p_data)
        
        # ML Prediction
        if ml_model is not None:
            try:
                features = pd.DataFrame([{
                    'prev_burst_time': process.prev_burst_time,
                    'inter_arrival_time': 5, # Approximate or default
                    'priority': process.priority,
                    'process_type': process.process_type
                }])
                pred = ml_model.predict(features)[0]
                process.predicted_burst_time = max(1, pred)
            except Exception as e:
                process.predicted_burst_time = process.burst_time
        else:
            # Dummy prediction if model is missing
            process.predicted_burst_time = process.burst_time * 0.9 
            
        process_list.append(process)

    results = []
    
    # Run all algorithms for comparison
    results.append(fcfs(process_list))
    results.append(sjf(process_list))
    results.append(round_robin(process_list, quantum=req.time_quantum))
    results.append(priority_scheduling(process_list))
    results.append(ml_hybrid_scheduler(process_list, quantum=req.time_quantum))
    
    return {"results": results}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "model_loaded": ml_model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

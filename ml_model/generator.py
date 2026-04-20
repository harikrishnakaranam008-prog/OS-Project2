import pandas as pd
import numpy as np
import os

def generate_historical_data(num_samples=5000, output_path="../data/dataset.csv"):
    """Generates synthetic historical process execution data."""
    np.random.seed(42)
    
    # Features:
    # - prev_burst_time: The burst time of the process in its previous CPU cycle
    # - inter_arrival_time: Time since the last process arrived
    # - priority: 1 (High) to 5 (Low)
    # - process_type: 0 (CPU-bound), 1 (I/O-bound), 2 (Mixed)
    
    data = []
    for _ in range(num_samples):
        process_type = np.random.choice([0, 1, 2], p=[0.4, 0.4, 0.2])
        
        if process_type == 0:  # CPU-bound
            actual_burst = int(np.random.normal(loc=15, scale=5))
            prev_burst = int(np.random.normal(loc=14, scale=6))
        elif process_type == 1:  # I/O-bound
            actual_burst = int(np.random.normal(loc=4, scale=2))
            prev_burst = int(np.random.normal(loc=5, scale=2))
        else:  # Mixed
            actual_burst = int(np.random.normal(loc=8, scale=4))
            prev_burst = int(np.random.normal(loc=8, scale=4))
            
        # Ensure positive burst times
        actual_burst = max(1, actual_burst)
        prev_burst = max(1, prev_burst)
        
        inter_arrival = max(0, int(np.random.normal(loc=5, scale=3)))
        priority = np.random.randint(1, 6)
        
        data.append([prev_burst, inter_arrival, priority, process_type, actual_burst])
        
    df = pd.DataFrame(data, columns=['prev_burst_time', 'inter_arrival_time', 'priority', 'process_type', 'actual_burst_time'])
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} samples at {output_path}")
    return df

if __name__ == "__main__":
    generate_historical_data()

import pandas as pd
import numpy as np
import os
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from generator import generate_historical_data

def train_model(data_path="../data/dataset.csv", model_path="model.pkl"):
    print("Loading data...")
    if not os.path.exists(data_path):
        print("Data not found. Generating...")
        generate_historical_data(output_path=data_path)
        
    df = pd.read_csv(data_path)
    
    X = df[['prev_burst_time', 'inter_arrival_time', 'priority', 'process_type']]
    y = df['actual_burst_time']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    
    print(f"Model Evaluation:\nMAE: {mae:.2f}\nRMSE: {rmse:.2f}")
    
    # Save the model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_path}")
    
if __name__ == "__main__":
    train_model()

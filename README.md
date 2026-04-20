# Intelligent CPU Scheduler using Machine Learning

A complete production-ready system that predicts CPU burst times using Machine Learning to optimize scheduling decisions.

## Project Structure
- `/backend`: FastAPI Python application with simulation logic.
- `/frontend`: React Dashboard with Vite.
- `/ml_model`: Script to generate training data and train the ML model.
- `/data`: Historical datasets.

## How to Run

### 1. Train the ML Model
Before running the backend, you must generate data and train the model.
```bash
cd ml_model
pip install pandas numpy scikit-learn
python train.py
```
This will create a `model.pkl` and a dataset in `/data/dataset.csv`.

### 2. Start Backend
The backend runs the scheduling simulation and serves the ML model predictions.
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Server runs on `http://localhost:8000`.

### 3. Start Frontend
The frontend provides the interactive visualization dashboard.
```bash
cd frontend
npm install
npm run dev
```
Dashboard runs on `http://localhost:5173`.

# MLOps Drift Detection Pipeline

An end-to-end Machine Learning Operations pipeline featuring automated model training, a live asynchronous prediction API, and statistical data drift monitoring. 

Built completely from scratch to simulate production traffic, detect malicious data shifts, and trigger automated alerts using Kolmogorov-Smirnov tests.

## Architecture Overview
* **Model Registry & Tracking:** `MLflow` (Containerized via Docker)
* **Prediction Engine:** `XGBoost` Classifier
* **Live Serving API:** `FastAPI` & `Uvicorn`
* **Data Drift Watchdog:** `Evidently AI`

## How It Works
1. **`train.py`:** Generates baseline network telemetry data and trains an XGBoost model, logging parameters and artifacts to a local MLflow tracking server.
2. **`app.py`:** A FastAPI application that pulls the latest model directly from MLflow and exposes a `/predict` endpoint to score live traffic.
3. **`simulate.py`:** Blasts the API with normal baseline traffic, then aggressively shifts the data distribution to simulate an attack, saving logs to `production.csv`.
4. **`monitor.py`:** Computes the statistical distance between the baseline and production logs. If the drift crosses the critical threshold, the Watchdog throws an automated system alert.

## Local Quickstart
Ensure Docker is running, then execute the pipeline:
```bash
# 1. Start the MLflow Server
docker compose up -d

# 2. Train and Register the Model
python src/train.py

# 3. Start the Live API (In a separate terminal)
python -m uvicorn src.app:app --reload

# 4. Run the Attack Simulator
python src/simulate.py

# 5. Trigger the Drift Watchdog
python src/monitor.py

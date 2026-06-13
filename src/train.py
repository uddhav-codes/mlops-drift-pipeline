import pandas as pd
import numpy as np
import xgboost as xgb
import mlflow
import mlflow.xgboost
import os

def generate_baseline_data():
    # Guarantee the folder exists
    os.makedirs("data", exist_ok=True)
    
    # Normal traffic: packet_size ~500, req_frequency ~30
    normal = pd.DataFrame({
        "packet_size": np.random.normal(500, 50, 800),
        "req_frequency": np.random.normal(30, 5, 800),
        "label": 0
    })
    # Anomaly traffic (Attack): packet_size > 650, freq > 45
    anomaly = pd.DataFrame({
        "packet_size": np.random.normal(700, 50, 200),
        "req_frequency": np.random.normal(50, 5, 200),
        "label": 1
    })
    df = pd.concat([normal, anomaly]).sample(frac=1).reset_index(drop=True)
    df.to_csv("data/baseline.csv", index=False)
    return df

if __name__ == "__main__":
    print("Generating baseline data...")
    df = generate_baseline_data()
    
    X = df[["packet_size", "req_frequency"]]
    y = df["label"]

    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Anomaly_Detection_Pipeline")

    with mlflow.start_run():
        print("Training XGBoost model...")
        model = xgb.XGBClassifier(n_estimators=100, max_depth=3)
        model.fit(X, y)
        
        # Register model into MLflow
        mlflow.xgboost.log_model(
            xgb_model=model,
            artifact_path="model",
            registered_model_name="AnomalyDetectorModel"
        )
        print("Baseline model trained & Registered in MLflow.")

import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc

app = FastAPI(title="Production ML Inference Service")

# Point to local MLflow Artifacts
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
model_name = "AnomalyDetectorModel"
stage = "latest" 

try:
    print("Attempting to load model from MLflow...")
    # Using the exact MLflow URI syntax for Version 1
    model = mlflow.pyfunc.load_model("models:/AnomalyDetectorModel/1")
    print("Model successfully loaded from MLflow!")
except Exception as e:
    print(f"MLflow Loading Error: {e}")
    model = None
class InferencePayload(BaseModel):
    packet_size: float
    req_frequency: float

@app.post("/predict")
def predict(payload: InferencePayload):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded or registered in MLflow yet.")
    
    input_data = pd.DataFrame([{
        "packet_size": payload.packet_size,
        "req_frequency": payload.req_frequency
    }])
    
    prediction = int(model.predict(input_data)[0])
    
    # Append to inference logs for drift analysis
    log_file = "data/production.csv"
    input_data['label'] = prediction # Storing predicted labels as placeholder context
    
    if not os.path.exists(log_file):
        input_data.to_csv(log_file, index=False)
    else:
        input_data.to_csv(log_file, mode='a', header=False, index=False)
        
    return {"prediction": prediction}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

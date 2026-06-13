import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def evaluate_drift():
    try:
        reference = pd.read_csv("data/baseline.csv").drop(columns=['label'])
        current = pd.read_csv("data/production.csv").drop(columns=['label'])
    except FileNotFoundError:
        print("Monitoring failed: Baseline or production logs missing.")
        return False

    # Configure Evidently Data Drift Profile
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(reference_data=reference, current_data=current)
    report_dict = data_drift_report.as_dict()

    # Extract statistical metric configurations
    drift_share = report_dict["metrics"][0]["result"]["share_of_drifted_columns"]
    dataset_drifted = report_dict["metrics"][0]["result"]["dataset_drift"]

    print(f"Percentage of features drifted: {drift_share * 100}%")
    print(f"Global Dataset Drift Status: {dataset_drifted}")

    if dataset_drifted:
        print("CRITICAL DRIFT DETECTED! Initiating automated pipeline fallback...")
        return True
    
    print("System metrics stable. No current drift detected.")
    return False

if __name__ == "__main__":
    evaluate_drift()

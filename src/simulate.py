import requests
import random
import time

API_URL = "http://127.0.0.1:8000/predict"

def send_traffic(packet_mean, freq_mean, iterations):
    for _ in range(iterations):
        payload = {
            "packet_size": random.gauss(packet_mean, 50),
            "req_frequency": random.gauss(freq_mean, 5)
        }
        try:
            requests.post(API_URL, json=payload)
        except requests.exceptions.ConnectionError:
            print("API offline! Start Uvicorn first.")
            return

if __name__ == "__main__":
    print("Phase 1: Sending normal traffic...")
    send_traffic(packet_mean=500, freq_mean=30, iterations=100)
    print("Phase 1 Complete.")
    
    time.sleep(1)
    
    print("Phase 2: Initiating simulated attack (Drifted traffic)...")
    send_traffic(packet_mean=850, freq_mean=60, iterations=100)
    print("Phase 2 Complete. Check the monitor!")

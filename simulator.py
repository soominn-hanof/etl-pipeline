import requests
import time
import sys

# The URL of our FastAPI endpoint
API_URL = "http://127.0.0.1:8000/generate/ecommerce"

def simulate_stream():
    print("🚀 Starting Data Stream Simulator...")
    print("Press Ctrl + C to stop.")
    
    try:
        count = 0
        while True:
            # Ping the API
            response = requests.get(API_URL)
            
            if response.status_code == 200:
                count += 1
                print(f"Record {count} pushed to Kafka.")
            else:
                print(f"Error: {response.status_code}")
                
            # Wait 0.5 seconds before pinging again
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n🛑 Stream stopped by user.")

if __name__ == "__main__":
    simulate_stream()

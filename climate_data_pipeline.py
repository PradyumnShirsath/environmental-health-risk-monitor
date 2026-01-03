import requests
import pandas as pd
from datetime import datetime
import time
import os

# --- CONFIGURATION ---
# We call this the "Ingestion Target"
DATA_STORE = "climate_history.csv" 
INTERVAL_SECONDS = 60  # Logs every 1 minute

# Strategic Monitoring Nodes
MONITORS = [
    {"name": "Sudan (Khartoum)", "lat": 15.5007, "lon": 32.5599},
    {"name": "New Delhi (India)", "lat": 28.6139, "lon": 77.2090},
    {"name": "London (UK)", "lat": 51.5074, "lon": -0.1278},
    {"name": "Beijing (China)", "lat": 39.9042, "lon": 116.4074},
    {"name": "Dubai (UAE)", "lat": 25.276987, "lon": 55.296249},
    {"name": "Ukraine (Kyiv)", "lat": 50.4501, "lon": 30.5234}
]

def fetch_telemetry(city):
    """
    Fetches real-time environmental metrics from Open-Meteo Satellite API.
    """
    try:
        # 1. Fetch Weather Data
        url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&current_weather=true&hourly=relativehumidity_2m"
        res = requests.get(url).json()
        
        # 2. Fetch Air Quality Data
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={city['lat']}&longitude={city['lon']}&current=us_aqi"
        aqi_res = requests.get(aqi_url).json()

        # 3. Structure the Data Packet
        return {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Location": city['name'],
            "Temperature_C": res['current_weather']['temperature'],
            "Humidity_Pct": res['hourly']['relativehumidity_2m'][0],
            "AQI_US": aqi_res['current']['us_aqi'],
            "Wind_Speed_kmh": res['current_weather']['windspeed']
        }
    except Exception as e:
        print(f"⚠️ Ingestion Failed for {city['name']}: {e}")
        return None

def execute_pipeline():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📡 Pipeline Active: Querying Satellites...")
    
    packet_buffer = []
    for city in MONITORS:
        data = fetch_telemetry(city)
        if data:
            packet_buffer.append(data)
            print(f"   ✅ Ingested: {city['name']}")

    # Commit to CSV Database
    df = pd.DataFrame(packet_buffer)
    file_exists = os.path.isfile(DATA_STORE)
    
    # If file exists, append without header. If new, add header.
    df.to_csv(DATA_STORE, mode='a', header=not file_exists, index=False)
    
    print(f"💾 Batch committed to: {DATA_STORE}\n")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🚀 Climate Data Pipeline Initialized.")
    print(f"📁 Storage Target: {DATA_STORE}")
    print("-" * 40)

    try:
        while True:
            execute_pipeline()
            # Wait for next cycle
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n🛑 Pipeline Deactivated.")
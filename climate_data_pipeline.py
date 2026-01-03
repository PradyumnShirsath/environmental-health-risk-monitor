import requests
import pandas as pd
from datetime import datetime
import time
import os

# --- CONFIGURATION ---
DATA_STORE = "climate_history.csv" 
SOURCE_FILE = "world_cities.csv"  # <--- New Input Source
INTERVAL_SECONDS = 60  # Rate Limit Safety: Don't go faster than this!

def load_targets():
    """
    Reads the list of cities from the CSV file dynamically.
    """
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(SOURCE_FILE)
        # Convert it to a list of dictionaries for easier looping
        target_list = df.to_dict('records')
        print(f"🌍 Loaded {len(target_list)} monitoring targets from {SOURCE_FILE}")
        return target_list
    except FileNotFoundError:
        print(f"❌ Error: {SOURCE_FILE} not found. Please create it first.")
        return []

def fetch_telemetry(city):
    """
    Fetches real-time environmental metrics for a single target.
    """
    try:
        # API Rate Limit Protection: Small pause between requests
        time.sleep(0.2) 

        # 1. Fetch Weather
        url = f"https://api.open-meteo.com/v1/forecast?latitude={city['Lat']}&longitude={city['Lon']}&current_weather=true&hourly=relativehumidity_2m"
        res = requests.get(url).json()
        
        # 2. Fetch Air Quality
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={city['Lat']}&longitude={city['Lon']}&current=us_aqi"
        aqi_res = requests.get(aqi_url).json()

        # 3. Return Structured Data
        return {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Location": city['City'],
            "Temperature_C": res['current_weather']['temperature'],
            "Humidity_Pct": res['hourly']['relativehumidity_2m'][0],
            "AQI_US": aqi_res['current']['us_aqi'],
            "Wind_Speed_kmh": res['current_weather']['windspeed']
        }
    except Exception as e:
        # Don't crash the whole pipeline if one city fails
        print(f"⚠️ Failed: {city['City']} ({e})")
        return None

def execute_pipeline():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📡 Starting Global Scan...")
    
    # 1. Load Targets Dynamically
    monitors = load_targets()
    if not monitors: return

    packet_buffer = []
    
    # 2. Loop through all 50+ cities
    for i, city in enumerate(monitors):
        data = fetch_telemetry(city)
        if data:
            packet_buffer.append(data)
            # Print progress every 5 cities so we know it's working
            if i % 5 == 0:
                print(f"   ✅ Scanned: {city['City']}...")

    # 3. Save Data
    if packet_buffer:
        df = pd.DataFrame(packet_buffer)
        file_exists = os.path.isfile(DATA_STORE)
        df.to_csv(DATA_STORE, mode='a', header=not file_exists, index=False)
        print(f"💾 Batch of {len(packet_buffer)} records saved to {DATA_STORE}")

# --- MAIN ENGINE ---
if __name__ == "__main__":
    print("🚀 Global Climate Data Pipeline Initialized.")
    print(f"📂 Reading Targets: {SOURCE_FILE}")
    print(f"📂 Writing Data:    {DATA_STORE}")
    print("-" * 40)

    try:
        while True:
            execute_pipeline()
            # Wait for next cycle
            print(f"💤 Cooling down for {INTERVAL_SECONDS} seconds...")
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n🛑 Pipeline Deactivated.")
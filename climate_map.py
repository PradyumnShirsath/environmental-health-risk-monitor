import folium
from folium.plugins import HeatMap
import requests
import pandas as pd  # <--- Now we use Pandas to read the CSV
import time
import math

# --- CONFIGURATION ---
CITY_SOURCE = "world_cities.csv"
SESSION = requests.Session()

# --- DATASET 1: CRISIS ZONES (Keep these hardcoded as they have special metadata) ---
CRISIS_ZONES = [
    ["Sudan (Khartoum)", 15.5007, 32.5599, 1100000, 8.5, "Extreme Drought"],
    ["Syria (Zaatari)", 32.2930, 36.3280, 6500000, 7.8, "Water Scarcity"],
    ["Bangladesh (Cox's Bazar)", 21.4272, 92.0058, 960000, 9.2, "Flood & Cyclone"],
    ["Afghanistan (Kabul)", 34.5553, 69.2075, 2800000, 8.1, "Food Insecurity"],
    ["Somalia (Dadaab)", 0.0514, 40.3040, 3000000, 9.0, "Famine Risk"],
    ["Ukraine (Kyiv)", 50.4501, 30.5234, 5900000, 3.5, "Conflict Zone"],
    ["Yemen (Sana'a)", 15.3694, 44.1910, 4500000, 8.9, "Water Collapse"],
    ["Haiti (Port-au-Prince)", 18.5944, -72.3074, 500000, 9.1, "Storms & Instability"]
]

def load_global_monitors():
    """Reads the CSV to get the list of 50+ Global Cities"""
    try:
        df = pd.read_csv(CITY_SOURCE)
        return df.to_dict('records')
    except FileNotFoundError:
        print("⚠️ Warning: world_cities.csv not found. Map will only show Crisis Zones.")
        return []

def calculate_wet_bulb(T, RH):
    """Stull's Formula for Wet Bulb Temperature"""
    try:
        tw = (T * math.atan(0.151977 * (RH + 8.313659)**(0.5))) + \
             (math.atan(T + RH)) - \
             (math.atan(RH - 1.676331)) + \
             (0.00391838 * (RH**(1.5)) * math.atan(0.023101 * RH)) - 4.686035
        return round(tw, 1)
    except:
        return None

def get_telemetry(lat, lon):
    try:
        # Rate limit protection
        time.sleep(0.1)
        
        # 1. Weather
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        w_res = SESSION.get(w_url, timeout=3).json()
        temp = w_res['current_weather']['temperature']
        humid = w_res['hourly']['relativehumidity_2m'][0]
        
        # 2. Bio-Metric Calculation
        wet_bulb = calculate_wet_bulb(temp, humid)

        # 3. Air Quality
        a_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm2_5"
        a_res = SESSION.get(a_url, timeout=3).json()
        aqi = a_res['current']['us_aqi']
        pm25 = a_res['current']['pm2_5']
        
        return temp, humid, wet_bulb, aqi, pm25
    except:
        return "N/A", "N/A", "N/A", "N/A", "N/A"

def generate_health_map():
    print("🔹 Initializing Environmental Health Engine...")
    
    # Create Base Map
    m = folium.Map(location=[20, 10], zoom_start=2, tiles='CartoDB dark_matter')
    heat_data = []

    # 1. Load Data Sources
    global_cities = load_global_monitors()
    print(f"🔹 Linking to Satellite Feeds ({len(CRISIS_ZONES) + len(global_cities)} nodes)...")

    # 2. Process Crisis Zones (Red Markers)
    for zone in CRISIS_ZONES:
        name, lat, lon, pop, risk, hazard = zone
        temp, humid, wet_bulb, aqi, pm25 = get_telemetry(lat, lon)
        
        if isinstance(temp, (int, float)):
             heat_data.append([lat, lon, 1.0]) # High intensity for crisis

        popup_html = f"""
        <div style="font-family:sans-serif; width:200px;">
            <h4 style="margin:0; border-bottom:2px solid #ff0033; color:#ff0033">{name}</h4>
            <b style="font-size:10px;">{hazard}</b><br>
            Temp: {temp}°C | WB: {wet_bulb}°C<br>
            AQI: {aqi} | PM2.5: {pm25}
        </div>
        """
        folium.CircleMarker(
            location=[lat, lon], radius=8, color='#ff0033', fill=True, fill_color='#ff0033',
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)

    # 3. Process Global Monitors from CSV (Green/Orange/Red Markers)
    for city in global_cities:
        name = city['City']
        lat = city['Lat']
        lon = city['Lon']
        
        temp, humid, wet_bulb, aqi, pm25 = get_telemetry(lat, lon)
        
        # Color Logic
        color = '#00ff00' # Green (Safe)
        if isinstance(aqi, (int, float)):
            if aqi > 100 or (isinstance(wet_bulb, float) and wet_bulb > 30):
                color = '#ff9900' # Orange
            if aqi > 150 or (isinstance(wet_bulb, float) and wet_bulb > 32):
                color = '#ff0000' # Red
            
            # Add to heatmap (intensity based on heat)
            if isinstance(temp, (int, float)):
                heat_data.append([lat, lon, temp/40]) 

        popup_html = f"""
        <div style="font-family:sans-serif; width:180px;">
            <h5 style="margin:0; border-bottom:1px solid {color};">{name}</h5>
            <span style="font-size:10px; color:#ccc;">Global Monitor</span><br>
            Temp: {temp}°C | WB: {wet_bulb}°C<br>
            AQI: {aqi}
        </div>
        """
        folium.CircleMarker(
            location=[lat, lon], radius=5, color=color, fill=True, fill_color=color, fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(m)
        
    # 4. Add Heatmap Layer
    if heat_data:
        HeatMap(heat_data, radius=15, blur=10).add_to(m)

    m.save("global_climate_dashboard.html")
    print(f"✅ MAP GENERATED: Tracking {len(CRISIS_ZONES) + len(global_cities)} locations.")

if __name__ == "__main__":
    generate_health_map()
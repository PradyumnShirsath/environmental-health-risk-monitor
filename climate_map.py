import folium
from folium.plugins import HeatMap
import requests
import branca.colormap as cm
import time
import math

# --- CONFIGURATION ---
SESSION = requests.Session()  # Reuses connections for speed

# --- DATASET 1: CRISIS ZONES (Displacement + Conflict) ---
CRISIS_ZONES = [
    ["Sudan (Khartoum)", 15.5007, 32.5599, 1100000, 8.5, "Extreme Drought"],
    ["Syria (Zaatari)", 32.2930, 36.3280, 6500000, 7.8, "Water Scarcity"],
    ["Bangladesh (Cox's Bazar)", 21.4272, 92.0058, 960000, 9.2, "Flood & Cyclone"],
    ["Afghanistan (Kabul)", 34.5553, 69.2075, 2800000, 8.1, "Food Insecurity"],
    ["Somalia (Dadaab)", 0.0514, 40.3040, 3000000, 9.0, "Famine Risk"],
    ["Ukraine (Kyiv)", 50.4501, 30.5234, 5900000, 3.5, "Conflict Zone"],
    ["Chad (N'Djamena)", 12.1348, 15.0557, 600000, 8.8, "Desertification"],
    ["Yemen (Sana'a)", 15.3694, 44.1910, 4500000, 8.9, "Water Collapse"],
    ["Turkey (Istanbul)", 41.0082, 28.9784, 3700000, 5.5, "Heat Stress"],
    ["Ethiopia (Addis Ababa)", 9.0331, 38.7444, 900000, 7.9, "Agricultural Failure"],
    ["Haiti (Port-au-Prince)", 18.5944, -72.3074, 500000, 9.1, "Storms & Instability"]
]

# --- DATASET 2: GLOBAL MONITORS ---
GLOBAL_CAPITALS = [
    ["USA (Washington DC)", 38.9072, -77.0369], ["UK (London)", 51.5074, -0.1278],
    ["France (Paris)", 48.8566, 2.3522], ["Germany (Berlin)", 52.5200, 13.4050],
    ["Russia (Moscow)", 55.7558, 37.6173], ["China (Beijing)", 39.9042, 116.4074],
    ["Japan (Tokyo)", 35.6762, 139.6503], ["India (New Delhi)", 28.6139, 77.2090],
    ["Brazil (Brasilia)", -15.8267, -47.9218], ["South Africa (Pretoria)", -25.7479, 28.2293],
    ["Australia (Canberra)", -35.2809, 149.1300], ["Canada (Ottawa)", 45.4215, -75.6972],
    ["Mexico (Mexico City)", 19.4326, -99.1332], ["Argentina (Buenos Aires)", -34.6037, -58.3816],
    ["Egypt (Cairo)", 30.0444, 31.2357], ["Nigeria (Abuja)", 9.0765, 7.3986],
    ["Indonesia (Jakarta)", -6.2088, 106.8456], ["Thailand (Bangkok)", 13.7563, 100.5018],
    ["Saudi Arabia (Riyadh)", 24.7136, 46.6753], ["Italy (Rome)", 41.9028, 12.4964],
    ["Singapore", 1.3521, 103.8198], ["Pakistan (Islamabad)", 33.6844, 73.0479]
]

def calculate_wet_bulb(T, RH):
    """
    Calculates Wet Bulb Temperature using Stull's formula (2011).
    Critical Health Metric: >32C is dangerous, >35C is survivability limit.
    """
    try:
        tw = (T * math.atan(0.151977 * (RH + 8.313659)**(0.5))) + \
             (math.atan(T + RH)) - \
             (math.atan(RH - 1.676331)) + \
             (0.00391838 * (RH**(1.5)) * math.atan(0.023101 * RH)) - 4.686035
        return round(tw, 1)
    except:
        return "N/A"

def get_telemetry(lat, lon):
    try:
        # 1. Weather
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        w_res = SESSION.get(w_url, timeout=3).json()
        temp = w_res['current_weather']['temperature']
        humid = w_res['hourly']['relativehumidity_2m'][0]
        wind = w_res['current_weather']['windspeed']
        
        # 2. Bio-Metric Calculation
        wet_bulb = calculate_wet_bulb(temp, humid)

        # 3. Air Quality
        a_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm2_5"
        a_res = SESSION.get(a_url, timeout=3).json()
        aqi = a_res['current']['us_aqi']
        pm25 = a_res['current']['pm2_5']
        
        return temp, humid, wind, wet_bulb, aqi, pm25
    except:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

def generate_health_map():
    print("🔹 Initializing Environmental Health Engine...")
    m = folium.Map(location=[20, 10], zoom_start=2, tiles='CartoDB dark_matter')
    
    # Heatmap Data Collector
    heat_data = []

    print(f"🔹 Linking to Satellite Feeds ({len(CRISIS_ZONES) + len(GLOBAL_CAPITALS)} nodes)...")
    
    # Process All Locations
    all_locations = [(x, 'crisis') for x in CRISIS_ZONES] + [(x, 'monitor') for x in GLOBAL_CAPITALS]
    
    for loc_data, l_type in all_locations:
        if l_type == 'crisis':
            name, lat, lon, pop, risk, hazard = loc_data
            color = '#ff0033' # Red
            tag = "CRISIS ZONE"
        else:
            name, lat, lon = loc_data
            color = '#00ff00' # Green (default)
            tag = "GLOBAL MONITOR"
            pop, risk, hazard = "N/A", "N/A", "N/A"

        # Fetch Live Data
        temp, humid, wind, wet_bulb, aqi, pm25 = get_telemetry(lat, lon)
        
        # Add to Heatmap (Weight by Temperature)
        if isinstance(temp, (int, float)):
            heat_data.append([lat, lon, temp/50]) # Normalize temp for heatmap intensity

        # Color Logic for Monitors (Dynamic Health Warning)
        if l_type == 'monitor' and isinstance(aqi, (int, float)):
            if aqi > 100 or (isinstance(wet_bulb, float) and wet_bulb > 30):
                color = '#ff9900' # Orange (Warning)
            if aqi > 150 or (isinstance(wet_bulb, float) and wet_bulb > 32):
                color = '#ff0000' # Red (Danger)

        # Medical Popup
        wb_warning = "⚠️" if isinstance(wet_bulb, float) and wet_bulb > 30 else ""
        
        popup_html = f"""
        <div style="font-family:sans-serif; width:220px;">
            <h4 style="margin:0; border-bottom:2px solid {color};">{name}</h4>
            <span style="font-size:10px; background:{color}; color:black; padding:1px 4px; border-radius:3px;">{tag}</span>
            
            <div style="margin-top:8px; font-size:11px; line-height:1.4;">
                <b>🌡️ Temp:</b> {temp}°C <br>
                <b>💧 Humidity:</b> {humid}% <br>
                <b>🔥 Wet Bulb:</b> {wet_bulb}°C {wb_warning}<br>
                <hr style="margin:4px 0; border:0; border-top:1px solid #444;">
                <b>🏭 AQI:</b> {aqi} | <b>PM2.5:</b> {pm25}<br>
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=6 if l_type == 'monitor' else pop/200000 + 4,
            popup=folium.Popup(popup_html, max_width=250),
            color=color,
            fill=True, fill_color=color, fill_opacity=0.7, weight=1
        ).add_to(m)
        
        time.sleep(0.05) # Rate limit protection

    # Add Thermal Layer
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)
    
    # Legend
    legend_html = '''
    <div style="position: fixed; bottom: 30px; left: 30px; width: 300px; 
    background: rgba(0,0,0,0.8); color: white; padding: 10px; border: 1px solid #444; font-size:12px;">
    <b>🏥 Health Risk Surveillance</b><br>
    <i style="color:#ccc;">Live Data: Temp, AQI, Wet Bulb</i><br>
    <span style="color:#ff0033">●</span> Crisis / Dangerous Environment<br>
    <span style="color:#00ff00">●</span> Safe Environmental Limits<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save("global_climate_dashboard.html")
    print("\n✅ SYSTEM UPGRADE COMPLETE: Wet Bulb Metrics + Thermal Layer Active.")

if __name__ == "__main__":
    generate_health_map()
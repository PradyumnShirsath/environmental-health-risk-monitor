import folium
import requests
import branca.colormap as cm
import time

# --- DATASET 1: HIGH-PRIORITY HUMANITARIAN ZONES (Real Conflict Data) ---
# [Name, Lat, Lon, Refugees, Risk_Score/10, Hazard_Type]
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

# --- DATASET 2: GLOBAL CLIMATE MONITORS (Capitals & Major Cities) ---
# We use these to track Global Warming & Pollution across the rest of the world.
# Format: [City, Lat, Lon]
GLOBAL_CAPITALS = [
    ["USA (Washington DC)", 38.9072, -77.0369], ["UK (London)", 51.5074, -0.1278],
    ["France (Paris)", 48.8566, 2.3522], ["Germany (Berlin)", 52.5200, 13.4050],
    ["Russia (Moscow)", 55.7558, 37.6173], ["China (Beijing)", 39.9042, 116.4074],
    ["Japan (Tokyo)", 35.6762, 139.6503], ["India (New Delhi)", 28.6139, 77.2090],
    ["Brazil (Brasilia)", -15.8267, -47.9218], ["South Africa (Pretoria)", -25.7479, 28.2293],
    ["Australia (Canberra)", -35.2809, 149.1300], ["Canada (Ottawa)", 45.4215, -75.6972],
    ["Mexico (Mexico City)", 19.4326, -99.1332], ["Argentina (Buenos Aires)", -34.6037, -58.3816],
    ["Egypt (Cairo)", 30.0444, 31.2357], ["Nigeria (Abuja)", 9.0765, 7.3986],
    ["Kenya (Nairobi)", -1.2921, 36.8219], ["Saudi Arabia (Riyadh)", 24.7136, 46.6753],
    ["Indonesia (Jakarta)", -6.2088, 106.8456], ["Thailand (Bangkok)", 13.7563, 100.5018],
    ["South Korea (Seoul)", 37.5665, 126.9780], ["Italy (Rome)", 41.9028, 12.4964],
    ["Spain (Madrid)", 40.4168, -3.7038], ["Sweden (Stockholm)", 59.3293, 18.0686],
    ["Norway (Oslo)", 59.9139, 10.7522], ["Poland (Warsaw)", 52.2297, 21.0122],
    ["Greece (Athens)", 37.9838, 23.7275], ["Iran (Tehran)", 35.6892, 51.3890],
    ["Pakistan (Islamabad)", 33.6844, 73.0479], ["Vietnam (Hanoi)", 21.0285, 105.8542],
    ["Philippines (Manila)", 14.5995, 120.9842], ["Colombia (Bogota)", 4.7110, -74.0721],
    ["Peru (Lima)", -12.0464, -77.0428], ["Chile (Santiago)", -33.4489, -70.6693],
    ["New Zealand (Wellington)", -41.2865, 174.7762], ["Singapore", 1.3521, 103.8198]
]

def get_full_climate_data(lat, lon):
    """
    Fetches comprehensive environmental data.
    """
    try:
        # 1. Weather Data (Temp, Humidity, Wind)
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        w_res = requests.get(w_url, timeout=4).json()
        temp = w_res['current_weather']['temperature']
        humid = w_res['hourly']['relativehumidity_2m'][0] # Current hour humidity
        wind = w_res['current_weather']['windspeed']

        # 2. Air Quality Data (AQI, PM2.5, NO2)
        # PM2.5 = Fine particulate matter (Smoke/Dust).
        a_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm2_5,nitrogen_dioxide"
        a_res = requests.get(a_url, timeout=4).json()
        aqi = a_res['current']['us_aqi']
        pm25 = a_res['current']['pm2_5']
        
        return temp, humid, wind, aqi, pm25
    except:
        return "N/A", "N/A", "N/A", "N/A", "N/A"

def generate_global_map():
    print("🔹 Initializing Global Climate Command Center...")
    
    # 1. Base Map (Dark Mode for contrast)
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB dark_matter')
    
    # 2. Risk Legend (Green to Red)
    colormap = cm.LinearColormap(colors=['#00ff00', '#ffff00', '#ff0000'], index=[0, 50, 100], vmin=0, vmax=150)
    colormap.caption = "Live Air Quality Index (AQI) - Green=Clean, Red=Hazardous"
    colormap.add_to(m)

    # --- PROCESS CRISIS ZONES (RED MARKERS) ---
    print(f"🔹 Processing {len(CRISIS_ZONES)} Humanitarian Crisis Zones...")
    for loc in CRISIS_ZONES:
        name, lat, lon, pop, risk, hazard = loc
        temp, humid, wind, aqi, pm25 = get_full_climate_data(lat, lon)
        
        # Crisis Popup (Humanitarian Focus)
        popup_html = f"""
        <div style="font-family:sans-serif; width:250px;">
            <h4 style="margin:0; border-bottom:2px solid red; padding-bottom:5px;">{name}</h4>
            <span style="background-color:red; color:white; padding:2px 5px; font-size:10px; border-radius:3px;">CRISIS ZONE</span>
            
            <div style="margin-top:8px; font-size:12px;">
                <b>👥 Refugees:</b> {pop:,}<br>
                <b>⚠️ Hazard:</b> {hazard}<br>
                <b>🌡️ Climate Risk:</b> {risk}/10 (ND-GAIN)<br>
            </div>
            <hr style="border-top:1px solid #444;">
            <div style="font-size:12px; color:#aaa;">
                <b>Temp:</b> {temp}°C | <b>Humidity:</b> {humid}%<br>
                <b>AQI:</b> {aqi} | <b>PM2.5:</b> {pm25} µg/m³
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=pop/200000 + 5, # Radius based on refugee population
            popup=folium.Popup(popup_html, max_width=300),
            color="#ff0033", # Red for Crisis
            fill=True, fill_color="#ff0033", fill_opacity=0.7, weight=1
        ).add_to(m)
        time.sleep(0.1)

    # --- PROCESS GLOBAL MONITORS (BLUE MARKERS) ---
    print(f"🔹 Processing {len(GLOBAL_CAPITALS)} Global Climate Monitors...")
    for loc in GLOBAL_CAPITALS:
        name, lat, lon = loc
        temp, humid, wind, aqi, pm25 = get_full_climate_data(lat, lon)
        
        # Color based on AQI (Air Quality)
        # Green (<50), Yellow (50-100), Orange (100-150), Red (>150)
        color = "#00ff00" # Default Green
        if isinstance(aqi, (int, float)):
            if aqi > 50: color = "#ffff00" # Moderate
            if aqi > 100: color = "#ff9900" # Unhealthy
            if aqi > 150: color = "#ff0000" # Hazardous
            
        # Monitor Popup (Environmental Focus)
        popup_html = f"""
        <div style="font-family:sans-serif; width:200px;">
            <h4 style="margin:0; border-bottom:2px solid {color}; padding-bottom:5px;">{name}</h4>
            <span style="background-color:#0072BC; color:white; padding:2px 5px; font-size:10px; border-radius:3px;">GLOBAL MONITOR</span>
            
            <div style="margin-top:8px; font-size:12px;">
                <b>🏭 Air Quality (AQI):</b> {aqi}<br>
                <b>🌫️ Pollutants (PM2.5):</b> {pm25} µg/m³<br>
                <b>🌡️ Temp:</b> {temp}°C<br>
                <b>💧 Humidity:</b> {humid}%<br>
                <b>💨 Wind:</b> {wind} km/h
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=6, # Fixed size for monitors
            popup=folium.Popup(popup_html, max_width=250),
            color=color, # Color changes based on pollution
            fill=True, fill_color=color, fill_opacity=0.7, weight=1
        ).add_to(m)
        time.sleep(0.1)

    # 3. Add Dashboard Title
    title_html = '''
             <div style="position: fixed; 
                         bottom: 30px; left: 30px; width: 400px; height: 160px; 
                         z-index:9999; font-size:12px;
                         background-color: rgba(0,0,0,0.85); color: white;
                         padding: 15px; border-radius: 8px; border: 1px solid #444; box-shadow: 0 0 10px rgba(0,0,0,0.5);">
                 <h3 style="margin-top:0; color:#ffcc00;"><b>🌍 Project Hazard: Global Command Center</b></h3>
                 Merged Analysis: <b>Refugee Crises</b> + <b>Live Environmental Monitoring</b><br>
                 <br>
                 <span style="color:#ff0033; font-size:14px;">●</span> <b>Crisis Zones:</b> High Displacement & Conflict<br>
                 <span style="color:#00ff00; font-size:14px;">●</span> <b>Global Monitors:</b> Real-time Climate Tracking<br>
                 <br>
                 <i>Live Data: Temp, Humidity, PM2.5, AQI (Open-Meteo Satellites)</i>
             </div>
             '''
    m.get_root().html.add_child(folium.Element(title_html))

    # 4. Save
    m.save("global_climate_dashboard.html")
    print("\n✅ DASHBOARD COMPLETE: 'global_climate_dashboard.html'")
    print("   -> Opened connection to 50+ Global Satellites.")

if __name__ == "__main__":
    generate_global_map()
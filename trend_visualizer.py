import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
import os

# --- CONFIGURATION ---
DATA_FILE = "climate_history.csv"
OUTPUT_IMAGE = "climate_trends_report.png"
CITIES_TO_COMPARE = ["New Delhi (India)", "London (UK)", "Tokyo (Japan)", "Dubai (UAE)"]

def generate_report():
    print("📊 Initializing Trend Analysis Engine...")
    
    # 1. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: Database {DATA_FILE} not found. Run the pipeline first.")
        return

    df = pd.read_csv(DATA_FILE)
    
    # Convert Timestamp to DateTime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Filter for selected cities only
    df_filtered = df[df['Location'].isin(CITIES_TO_COMPARE)]

    if df_filtered.empty:
        print("⚠️ Not enough data yet. Run the pipeline for a few minutes first!")
        return

    # 2. Setup "Cyberpunk" Dark Style
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Custom color palette
    palette = sns.color_palette("bright", n_colors=len(CITIES_TO_COMPARE))

    # --- PLOT 1: TEMPERATURE TRENDS ---
    sns.lineplot(data=df_filtered, x='Timestamp', y='Temperature_C', hue='Location', 
                 ax=ax1, palette=palette, linewidth=2.5, marker='o')
    
    ax1.set_title("🌡️ Thermal Variance Analysis (Live)", fontsize=16, fontweight='bold', color='#00ffcc')
    ax1.set_ylabel("Temperature (°C)", fontsize=12)
    ax1.grid(color='gray', linestyle=':', linewidth=0.5)
    ax1.legend(loc='upper right', frameon=True, facecolor='#222')

    # --- PLOT 2: AIR QUALITY TRENDS ---
    sns.lineplot(data=df_filtered, x='Timestamp', y='AQI_US', hue='Location', 
                 ax=ax2, palette=palette, linewidth=2.5, marker='s')
    
    ax2.set_title("🏭 Air Toxicity Levels (AQI)", fontsize=16, fontweight='bold', color='#ff0033')
    ax2.set_ylabel("AQI Score", fontsize=12)
    ax2.set_xlabel("Time (UTC)", fontsize=12)
    ax2.grid(color='gray', linestyle=':', linewidth=0.5)
    
    # Add Critical Threshold Line for AQI
    ax2.axhline(y=150, color='red', linestyle='--', linewidth=1, label="Unhealthy Threshold")
    ax2.text(df_filtered['Timestamp'].min(), 155, 'CRITICAL LIMIT', color='red', fontsize=10)
    
    # Format Time Axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    
    # 3. Save Report
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=300, bbox_inches='tight')
    print(f"✅ Analysis Complete. Report generated: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    generate_report()
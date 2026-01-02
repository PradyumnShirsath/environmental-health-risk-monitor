# Project Sentinel: Environmental Health Risk Monitor

![Status](https://img.shields.io/badge/Status-Live_Bio_Surveillance-success?style=flat-square)
![Domain](https://img.shields.io/badge/Domain-Public_Health-red?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Environmental_Determinants-green?style=flat-square)

## 🏥 Abstract: The Environmental Determinants of Health
According to the WHO, environmental factors are responsible for 24% of the global burden of disease. **Project Sentinel** is a **Real-Time Health Surveillance System** designed to track these external threats.

By integrating **Satellite Telemetry** (Air Quality/Heat) with **Geopolitical Data** (Displacement/Conflict), this dashboard provides a holistic view of the "Exposome"—the total environmental exposure affecting human health in real-time.

---

## 🩺 Visual Intelligence: The Health Risk Matrix
### The Dashboard Architecture
This tool monitors the **Triple Burden of Risk**:

* **🫁 Respiratory Health (AQI & PM2.5)**
    * **Live Sensor Data:** Tracks PM2.5 levels (microscopic particulates) via Open-Meteo satellites.
    * **Medical Impact:** Identifies zones with hazardous air quality linked to asthma, COPD, and cardiovascular failure.

* **🌡️ Thermal Stress (Temp & Humidity)**
    * **Wet Bulb Proxy:** Monitors the combination of Heat + High Humidity.
    * **Medical Impact:** Predicts "Hyperthermia" risk (Heatstroke) and dehydration events in vulnerable populations.

* **⚠️ Physical Safety (Conflict & Displacement)**
    * **Crisis Zones:** Tracks refugee density in high-conflict regions (e.g., Sudan, Syria).
    * **Social Determinant:** Proxies for sanitation collapse, malnutrition risk, and trauma.

---

## 🛠️ Methodology & Data Sources
The system utilizes a **Bio-Geospatial Engine** to render health risks on a global scale.

| Risk Factor | Data Source | Health Implication |
| :--- | :--- | :--- |
| **Particulate Matter (PM2.5)** | Open-Meteo Air Quality API | Lung Disease / Cancer Risk |
| **Nitrogen Dioxide (NO2)** | Open-Meteo Air Quality API | Urban Smog / Respiratory Irritation |
| **Relative Humidity** | Open-Meteo Weather API | Heat Stress Index (Body cooling failure) |
| **Conflict Intensity** | UNHCR Displacement Data | Injury / Infectious Disease Outbreak |

---

## 📂 Repository Structure
| File Name | Description |
| :--- | :--- |
| `climate_map.py` | **The Bio-Engine.** Fetches live satellite data and maps it against health risk thresholds. |
| `global_climate_dashboard.html` | **The Health Monitor.** Interactive dashboard visualizing global health threats. |
| `requirements.txt` | **Dependencies.** Python geospatial and request libraries. |

---

## 🚀 Usage Instructions
### Prerequisites
* Python 3.8+
* Internet connection (for Live Satellite Feeds)

### Setup & Execution
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/PradyumnShirsath/environmental-health-risk-monitor.git](https://github.com/PradyumnShirsath/environmental-health-risk-monitor.git)
    cd environmental-health-risk-monitor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Surveillance:**
    ```bash
    python climate_map.py
    ```
    *The system will connect to global satellite feeds and generate `global_climate_dashboard.html`.*

---
*Author: Pradyumn Shirsath | Developed for Public Health & Environmental Research*
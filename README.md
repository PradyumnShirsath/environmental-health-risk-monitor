# 🌍 Sentinel: Environmental Health Bio-Surveillance System

<div align="center">

![Status](https://img.shields.io/badge/Status-Operational-success?style=for-the-badge&logo=statuspage)
![Language](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Domain](https://img.shields.io/badge/Domain-Public_Health_%26_Climate_Security-red?style=for-the-badge&logo=medrt)
![Pipeline](https://img.shields.io/badge/Data_Engineering-Automated_ETL-orange?style=for-the-badge&logo=airflow)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br>

**A Full-Stack Data Intelligence Platform** that aggregates real-time satellite telemetry to detect environmental health threats (Hyperthermia, AQI Toxicity) across 50+ global metropolitan hubs.

[View Demo](#-visual-intelligence) • [Installation](#-quick-start-guide) • [Architecture](#%EF%B8%8F-system-architecture)

</div>

---

## 📖 Executive Summary

According to the WHO, environmental factors are responsible for **24% of the global burden of disease**. Standard weather tools fail to correlate raw metrics with human physiological limits.

**Sentinel** is an automated **Bio-Surveillance Engine** designed to bridge this gap. It acts as a "Planetary Black Box," ingesting satellite data every 60 seconds to calculate medical risk metrics—specifically **Wet Bulb Temperature ($T_w$)** and **PM2.5 Toxicity**—to identify zones where the environment poses an immediate threat to human survival.

---

## ⚡ Key Features

*   **📡 Real-Time Bio-Surveillance**: Polls satellite APIs every 60 seconds to monitor environmental conditions in real-time.
*   **🌡️ Advanced Risk Metrics**: Calculates **Wet Bulb Temperature ($T_w$)** using the Stull (2011) formula to predict hyperthermia risk and correlates it with **PM2.5** data for respiratory toxicity.
*   **🌍 Geospatial Intelligence**: Generates interactive, high-fidelity maps (`global_climate_dashboard.html`) identifying "Crisis Zones" where environmental stress compounds with humanitarian issues.
*   **📊 Insightful Reporting**: Produces "Cyberpunk-style" executive reports (`climate_trends_report.png`) visualizing thermal variance and air toxicity trends over time.
*   **🛡️ Robust Data Engineering**: Features a decoupled ETL pipeline with built-in rate limiting, fault tolerance, and auto-recovery mechanisms.

---

## 🏗️ System Architecture

Sentinel utilizes a **Decoupled ETL (Extract, Transform, Load)** architecture to ensure scalability, fault tolerance, and data persistence.

```mermaid
graph TD
    subgraph Ingestion Layer [📡 Data Collection]
        A[Open-Meteo Satellite API] -->|JSON Stream| B(climate_data_pipeline.py)
        D[world_cities.csv] -->|Dynamic Config| B
    end
    
    subgraph Storage Layer [💾 Data Warehousing]
        B -->|Append Time-Series| C[(climate_history.csv)]
    end
    
    subgraph Intelligence Layer [🧠 Analytics & Viz]
        C -->|Read History| E(trend_visualizer.py)
        E -->|Matplotlib Engine| F[Analytics Report (PNG)]
        D -->|Read Config| G(climate_map.py)
        A -->|Real-time Feed| G
        G -->|Folium Engine| H[Interactive Dashboard (HTML)]
    end
```

### Tech Stack

*   **Core**: Python 3.9+
*   **Data Engineering**: `pandas`, `requests`
*   **Visualization**: `folium` (Geospatial), `matplotlib`, `seaborn` (Statistical)
*   **API**: Open-Meteo (Weather & Air Quality)

---

## 📊 Visual Intelligence

| **The Interactive Map** | **The Analytics Report** |
| :---: | :---: |
| *Real-time geospatial risk assessment* | *Longitudinal trend analysis* |
| ![Map](map_preview.png) | ![Graph](climate_trends_report.png) |

*(Note: Run the scripts locally to generate the latest visualizations)*

---

## 🛠️ Quick Start Guide

### Prerequisites
*   Python 3.8 or higher
*   `pip` package manager

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/PradyumnShirsath/environmental-health-risk-monitor.git
    cd environmental-health-risk-monitor
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Usage Guide

Sentinel operates in two phases: **Data Digestion** and **Intelligence Generation**.

### Phase 1: Data Digestion
Start the ETL pipeline to begin collecting data. This script runs continuously.

```bash
python climate_data_pipeline.py
```
> **Output**: Creates and populates `climate_history.csv` with real-time telemetry.

### Phase 2: Intelligence Generation
In a new terminal window, run the visualization engines to generate reports based on the collected data.

**Generate the Interactive Map:**
```bash
python climate_map.py
```
> **Output**: Generates `global_climate_dashboard.html`. Open this file in any web browser to explore global risk zones.

**Generate the Trend Report:**
```bash
python trend_visualizer.py
```
> **Output**: Generates `climate_trends_report.png`. A high-resolution image file visualizing temperature and AQI trends.

---

## 📂 Project Structure

```text
environmental-health-risk-monitor/
├── climate_data_pipeline.py  # Main ETL engine for data collection
├── climate_map.py            # Generates the interactive Folium map
├── trend_visualizer.py       # Generates static trend analysis charts
├── world_cities.csv          # Configuration file for monitoring targets
├── requirements.txt          # Python dependencies
├── climate_history.csv       # (Generated) Database of collected metrics
├── global_climate_dashboard.html # (Generated) Interactive map output
├── climate_trends_report.png # (Generated) Analytics report output
└── README.md                 # Project documentation
```

---

## 🔮 Future Roadmap

*   [ ] **Machine Learning**: Integration of LSTM neural networks to *forecast* AQI spikes 24h in advance.
*   [ ] **SMS Alerts**: Integration with Twilio API to push real-time health warnings to field agents.
*   [ ] **Cloud Deployment**: Containerization using Docker for seamless AWS/Azure deployment.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License & Contact

Distributed under the MIT License. See `LICENSE` for more information.

**Author**: Pradyumn Shirsath  
*Developed for Research in Computational Sustainability & Public Health*

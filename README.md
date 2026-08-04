# 🛰️ SatLink

> **Intelligent Satellite Communication Link Budget and Mission Analysis Platform**
>
> **Status:** Under Active Development

SatLink is an intelligent satellite communication and mission analysis platform designed to simplify the process of analyzing communication links between satellites and ground stations.

The platform enables users to perform end-to-end satellite link budget calculations by integrating mission configuration, orbital parameters, communication system design, and propagation analysis into a single, intuitive application. Built as an educational alternative to expensive commercial software, SatLink is intended for students, researchers, and aerospace engineers.

---

## Problem Statement

Before launching a satellite, engineers must verify that communication between the satellite and the ground station remains reliable throughout the mission. This requires performing a comprehensive **Link Budget Analysis**, which accounts for:

- 📡 Transmitter Power
- 📶 Antenna Gains
- 🌍 Free Space Path Loss
- ☁️ Atmospheric & Propagation Losses
- 📥 Receiver Sensitivity
- 🔊 System Noise
- 📈 Signal-to-Noise Ratio (SNR)
- 📊 Carrier-to-Noise Ratio (C/N)
- ✅ Link Margin

Existing industry-standard software such as **STK** and **MATLAB Aerospace Toolboxes** are powerful but expensive and often difficult for beginners.

SatLink aims to provide a modern, user-friendly, and open educational platform that makes satellite communication analysis accessible to everyone.

---

# Features

## Current Features

- Mission Configuration
- Link Budget Calculator
- Transmitter Modeling
- Receiver Modeling
- Antenna Gain Calculations
- Free Space Path Loss Calculation
- Atmospheric Loss Estimation
- Noise Analysis
- Carrier-to-Noise Ratio
- Signal-to-Noise Ratio
- Link Margin Calculation

---

## Planned Features

- Orbit Design Module
- Ground Station Coverage Analysis
- Doppler Shift Analysis
- BER (Bit Error Rate) Calculation
- Multiple Modulation Schemes
- Interactive Dashboards
- Mission Timeline
- PDF Report Generation
- CSV / Excel Export
- Multiple Ground Stations
- Multi-Satellite Support
- 3D Earth Visualization

---

# Tech Stack

### Programming Language
- Python

### Frontend
- Streamlit *(Planned)*

### Scientific Libraries
- NumPy
- SciPy
- Pandas
- Matplotlib
- Plotly

### Future Integrations
- Skyfield
- Poliastro
- Orekit

---

# Project Structure

```text
SatLink/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── mission/
│   ├── transmitter/
│   ├── receiver/
│   ├── antenna/
│   ├── propagation/
│   ├── calculations/
│   ├── visualization/
│   └── utilities/
│
├── assets/
├── data/
├── docs/
└── tests/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Ananyaaaa-12/SatLink.git
```

Navigate into the project

```bash
cd SatLink
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# Link Budget Parameters

SatLink performs calculations using parameters such as:

- Frequency
- Bandwidth
- Satellite Altitude
- Ground Station Coordinates
- Transmit Power
- Antenna Gain
- Cable Losses
- Atmospheric Attenuation
- Receiver Sensitivity
- Noise Temperature
- Data Rate
- Modulation Scheme
- Link Margin

---

# Objectives

- Make satellite communication analysis accessible.
- Provide an educational alternative to commercial software.
- Help students understand communication system design.
- Enable quick evaluation of satellite communication links.
- Integrate mission analysis into one unified platform.

---

# Roadmap

## Phase 1
- [ ] Project Setup
- [ ] User Interface
- [ ] Link Budget Calculator

## Phase 2
- [ ] Communication Modules
- [ ] Antenna Analysis
- [ ] Propagation Models
- [ ] Performance Metrics

## Phase 3
- [ ] Orbit Analysis
- [ ] Ground Station Coverage
- [ ] Interactive Visualizations

## Phase 4
- [ ] Mission Planner
- [ ] Report Generation
- [ ] Export Features
- [ ] Optimization Tools

---

# Contributors

- **Ananya N Rao**
- **Kevin Patel**

---

# License

This project is currently under development.

A license will be added in a future release.

---

# Acknowledgements

This project is inspired by:

- AGI Systems Tool Kit (STK)
- MATLAB Aerospace Toolbox
- NASA Communication System References
- ESA Mission Analysis Resources

---

### Building an accessible platform for satellite communication analysis.

**If you found this project interesting, consider giving it a ⭐ on GitHub!**

</div>

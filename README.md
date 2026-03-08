<div align="center">
  <img src="https://img.shields.io/badge/Blockchain-Simulation-darkgreen?style=for-the-badge&logo=hyperledger&logoColor=white" alt="Blockchain"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly"/>

  <h1>🐑 AgroLedger</h1>
  <p><strong>Blockchain-Powered Supply Chain Traceability Prototype for the Canadian Sheep Federation</strong></p>
</div>

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [UI/UX Design](#-uiux-design)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🌐 Live Demo
- **Status**: ✅ Operational
- **Streamlit Link**: [Launch AgroLedger Dashboard](https://streamlit.io/cloud) *(Update with your specific URL)*
- **Local Access**: `streamlit run app.py` (Port 8501)

---

## 🔭 Overview
**AgroLedger** is a premium, high-fidelity interactive prototype designed to simulate how **Hyperledger Fabric** blockchain technology enforces transparency, immutable traceability, and robust food safety across complex agricultural supply chains. 

Rather than deploying a live distributed ledger, this application emulates the exact events, data states, and interactions utilizing an advanced Python `Streamlit` Session State machine.

---

## ✨ Key Features
- **🌐 Global Admin Dashboard**: Real-time aggregated insights tracking active farms, registered livestock volumes, and the overall network node health metrics.
- **🔎 Immutable Traceability Timeline**: The core "Consumer Verification" module allows users to query a specific Sheep ID and visually trace its entire lifecycle—from Birth, to Veterinary Health Checks, through the Slaughterhouse, and finally to Retail.
- **🕸️ Commodity Flow Visualization**: Interactive, collision-detected network mapping representing the physical movement of commodities between distinct stakeholders.
- **🔐 Deep Role-Based Access Control**: Segmented interfaces utilizing Streamlit's multi-page setup for distinct roles:
  - **Producer**: Register new livestock and origin data.
  - **Veterinarian**: Issue immutable health certificates.
  - **Slaughterhouse**: Process livestock and log final meat weights.
  - **Consumer**: QR-style lookup for end-to-end transparency.

---

## 🏗️ Architecture & Tech Stack
- **Frontend Framework**: [Streamlit](https://streamlit.io/) (Multi-page configuration)
- **Data Visualization**: [Plotly Express](https://plotly.com/) & Plotly Graph Objects
- **Network Mapping**: `streamlit-agraph` for real-time node linking
- **Data Engineering**: Data structures powered by `Pandas` and internal Memory States.

---

## 📁 Project Structure

The repository is modularized strictly by Role-Based Access (via Streamlit pages) and backend utilities.

```text
AgroLedger/
├── 📄 app.py                     # [Global Admin] Network Snapshot, Metrics & Graph
├── 📄 requirements.txt           # Global Environment dependencies
├── 📁 pages/                     # Sub-applications for Access Roles
│   ├── 📄 1_Producer.py          # Local farm registration system
│   ├── 📄 2_Veterinarian.py      # Health certificate issuance
│   ├── 📄 3_Slaughterhouse.py    # Processing & weight logging
│   └── 📄 4_Consumer.py          # End-to-end QR code timeline
├── 📁 utils/
│   └── 📄 blockchain_state.py    # Core simulated ledger & state machine
└── 📁 .streamlit/
    └── 📄 config.toml            # Strict UI coloring palette
```

---

## 🚀 Installation & Setup

Ensure you have Python 3.9+ installed on your system.

**1. Clone the repository:**
```bash
git clone https://github.com/trithanhalan/AgroLedger.git
cd AgroLedger
```

**2. Initialize the Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Launch the Dashboard:**
```bash
streamlit run app.py
```

---

## 🖥️ Usage Guide

Upon launching `streamlit run app.py`, your browser will open to `localhost:8501`. 
1. **Admin Console**: You will immediately see the Global Dashboard. Review the network graphs and current livestock metrics.
2. **Role Navigation**: Use the left-hand sidebar to switch to different stakeholder views.
3. **Simulating Data**: Navigate to **Producer** and click "Register Sheep" to instantly simulate a blockchain transaction, then switch to the **Consumer** tab to search for that specific ID!

---

## 🎨 UI/UX Design (Superpowers Theme)
The frontend utilizes the elite **"Superpowers" UI/UX Methodology**. 
Instead of fragmented CSS hacks, the application relies on `.streamlit/config.toml` to enforce a strict **Dark Mode** backend paired with the Canadian Sheep Federation's precise brand colors:
- **Primary Accent**: Olive Green (`#7C8C03`)
- **Secondary Accent**: Earth Brown (`#695D46`)
- **Background Integrity**: Maximum contrast deep dark backgrounds (`#0E1117`) for extended viewer focus.

---

## 🛣️ Roadmap
- [ ] Direct IPFS storage simulation for health certificates.
- [ ] Integration of a local SQLite database to persist the mock blockchain state across reboots.
- [ ] QR code image generation for physical tagging.

---

## 📜 License
This proprietary prototype was developed exclusively for portfolio demonstration regarding agricultural traceability. All rights reserved by the original creator.

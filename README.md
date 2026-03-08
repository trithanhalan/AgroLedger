# AgroLedger: Blockchain Traceability Prototype

**AgroLedger** is a premium, high-fidelity prototype designed for the Canadian Sheep Federation, demonstrating how blockchain technology can enforce transparency, Traceability, and food safety across an entire agricultural supply chain.

## 🌟 Key Features

1. **Global Dashboard**: Aggregated insights on active farms, registered livestock, and the overall network traceability score.
2. **Immutable Traceability Timeline**: A "Consumer Verification" module allowing users to search a specific Sheep ID and visually track its journey from Birth to Retail.
3. **Network Visualization**: Interactive network mapping of commodity flow between farms, processors, and retailers.
4. **Role-Based Access**: Specialized interfaces for Global Admins, Farmers, and Consumers.

## 🛠 Tech Stack
- **Frontend**: Streamlit
- **Data Visualization**: Plotly Express, Plotly Graph Objects
- **Network Mapping**: Streamlit-Agraph
- **Data Handling**: Pandas

## 🚀 Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/trithanhalan/AgroLedger.git
   cd AgroLedger
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure
- `app.py`: The core Streamlit application containing the UI and mock data generation.
- `docs/`: Original documentation, Business Requirements Documents (BRDs), and presentations.
- `requirements.txt`: Python package dependencies.

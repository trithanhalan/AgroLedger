import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_agraph import agraph, Node, Edge, Config
import random
import datetime

# --- Configuration & Theme ---
st.set_page_config(
    page_title="AgroLedger | Prototype",
    page_icon="🐑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium dark theme look
st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    h1, h2, h3 {color: #4CAF50;}
    .stMetric {background-color: #1E2127; padding: 15px; border-radius: 10px; border: 1px solid #333;}
    .stTabs [data-baseweb="tab-list"] {gap: 20px;}
    .stTabs [data-baseweb="tab"] {height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 5px 5px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)


# --- Mock Data Generation ---
@st.cache_data
def generate_mock_data():
    farms = ["Sunrise Pastures", "Valley Farm", "Highland Sheep Co.", "Green Acres"]
    processors = ["Prime Cuts Ltd.", "Quality Meats", "Valley Processors"]
    retailers = ["FreshMart", "Premium Grocers", "Local Butcher"]
    
    data = []
    for _ in range(100):
        sheep_id = f"CFS-{random.randint(10000, 99999)}"
        birth_date = datetime.date.today() - datetime.timedelta(days=random.randint(100, 400))
        farm = random.choice(farms)
        processor = random.choice(processors) if random.random() > 0.3 else None
        retailer = random.choice(retailers) if processor and random.random() > 0.5 else None
        
        status = "At Farm"
        if retailer:
            status = "At Retail"
        elif processor:
            status = "Processing"
            
        data.append({
            "Sheep ID": sheep_id,
            "Birth Date": birth_date,
            "Origin Farm": farm,
            "Processor": processor,
            "Retailer": retailer,
            "Status": status,
            "Health Cert": "Verified" if random.random() > 0.1 else "Pending"
        })
    return pd.DataFrame(data)

df = generate_mock_data()

# --- App Header ---
st.title("🐑 AgroLedger")
st.markdown("*Blockchain-powered traceability for the Canadian Sheep Federation*")
st.info("ℹ️ **Prototype Disclaimer**: This Streamlit application serves as a high-fidelity **UI simulation** of the AgroLedger platform. It demonstrates the conceptual flow, data structures, and role-based access of the system. In a production environment, the 'Immutable Timeline' and records below would be connected to a live Web3 blockchain backend (e.g., Ethereum or Hyperledger) via Smart Contracts, rather than the simulated Python Pandas backend used here.")

# --- Sidebar (Role Selection) ---
with st.sidebar:
    st.header("Access Portal")
    role = st.selectbox("Select User Role", ["Global Overview (Admin)", "Farmer Dashboard", "Consumer Verification"])
    st.markdown("---")
    st.info("AgroLedger ensures supply chain transparency, food safety, and fair compensation using immutable ledger technology.")

# --- Main Content ---
if role == "Global Overview (Admin)":
    st.header("Global Network Dashboard")
    
    # 1. Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registered Livestock", len(df), "+12% this month")
    col2.metric("Active Farms", df["Origin Farm"].nunique(), "+2")
    col3.metric("Traceability Score", "98.5%", "+0.5%")
    col4.metric("Network Nodes", df["Origin Farm"].nunique() + df["Processor"].nunique() + df["Retailer"].nunique())

    st.markdown("---")
    
    # 2. Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Livestock Distribution by Farm")
        fig_pie = px.pie(df, names="Origin Farm", hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.Greens_r)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        st.subheader("Current Supply Chain Status")
        status_counts = df["Status"].value_counts().reset_index()
        fig_bar = px.bar(status_counts, x="Status", y="count", color="Status",
                         color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    
    # 3. Network Graph (Supply Chain Flow)
    st.subheader("Commodity Flow Network")
    nodes = []
    edges = []
    
    # Add Nodes
    for farm in df["Origin Farm"].dropna().unique():
        nodes.append( Node(id=farm, label=farm, size=25, color="#4CAF50") )
    for proc in df["Processor"].dropna().unique():
        nodes.append( Node(id=proc, label=proc, size=25, color="#FF9800") )
    for ret in df["Retailer"].dropna().unique():
        nodes.append( Node(id=ret, label=ret, size=25, color="#2196F3") )
        
    # Add Edges
    for idx, row in df.iterrows():
        if pd.notna(row['Origin Farm']) and pd.notna(row['Processor']):
            edges.append( Edge(source=row['Origin Farm'], target=row['Processor'], type="CURVE_SMOOTH") )
        if pd.notna(row['Processor']) and pd.notna(row['Retailer']):
            edges.append( Edge(source=row['Processor'], target=row['Retailer'], type="CURVE_SMOOTH") )
            
    config = Config(width=1000, height=400, directed=True, physics=True, hierarchical=False)
    agraph(nodes=nodes, edges=edges, config=config)

elif role == "Consumer Verification":
    st.header("Consumer Food Traceability")
    st.write("Enter the Sheep ID found on your product packaging to trace its origin.")
    
    search_id = st.text_input("🔍 Sheep ID (e.g., CFS-12345)", "")
    
    # Provide a hint
    st.caption(f"Hint: Try testing with {df['Sheep ID'].iloc[0]}")
    
    if search_id:
        result = df[df["Sheep ID"] == search_id]
        if not result.empty:
            item = result.iloc[0]
            st.success("✅ Authentic Record Found on Blockchain")
            
            # Interactive Timeline
            st.subheader("Immutable Timeline")
            
            stages = ["Birth & Registration", "Processing", "Retail"]
            dates = [
                str(item['Birth Date']), 
                str(item['Birth Date'] + datetime.timedelta(days=120)) if pd.notna(item['Processor']) else "N/A",
                str(item['Birth Date'] + datetime.timedelta(days=125)) if pd.notna(item['Retailer']) else "N/A"
            ]
            entities = [item['Origin Farm'], str(item['Processor']), str(item['Retailer'])]
            
            # Filter N/A
            valid_stages = []
            valid_dates = []
            valid_entities = []
            for s, d, e in zip(stages, dates, entities):
                if d != "N/A" and e != "None":
                    valid_stages.append(s)
                    valid_dates.append(d)
                    valid_entities.append(e)
            
            # Timeline Visualization
            fig_time = go.Figure(data=[
                go.Scatter(
                    x=valid_dates, 
                    y=[1]*len(valid_dates),
                    mode="lines+markers+text",
                    text=valid_stages,
                    textposition="top center",
                    hovertext=valid_entities,
                    marker=dict(size=20, color="#4CAF50", line=dict(width=3, color="white")),
                    line=dict(color="#4CAF50", width=4)
                )
            ])
            fig_time.update_layout(
                yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                xaxis=dict(showgrid=False),
                height=250,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            st.markdown(f"**Health Certificate:** {item['Health Cert']}")
        else:
            st.error("❌ Record not found. This item cannot be verified.")

else:
    # Farmer Dashboard
    st.header("Farm Operations")
    farm_options = df["Origin Farm"].unique()
    selected_farm = st.selectbox("Select Farm", farm_options)
    
    farm_data = df[df["Origin Farm"] == selected_farm]
    
    col1, col2 = st.columns(2)
    col1.metric("Total Herd Size", len(farm_data))
    col2.metric("Pending Health Certs", len(farm_data[farm_data["Health Cert"] == "Pending"]))
    
    st.subheader("Livestock Ledger")
    st.dataframe(farm_data[["Sheep ID", "Birth Date", "Status", "Health Cert"]], use_container_width=True)

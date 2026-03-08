import streamlit as st
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
from utils.blockchain_state import init_blockchain_state, get_theme_css, get_ledger

# --- Configuration & Theme ---
st.set_page_config(
    page_title="AgroLedger | Global Admin Dashboard",
    page_icon="🐑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_theme_css(), unsafe_allow_html=True)
init_blockchain_state()
df = get_ledger()

# --- App Header ---
st.title("🐑 AgroLedger Global Dashboard")
st.markdown("*Blockchain-powered traceability for the Canadian Sheep Federation*")
st.info("ℹ️ **Prototype Disclaimer**: This is a multi-page Streamlit application simulating the AgroLedger Hyperledger Fabric implementation. Use the sidebar to navigate between different stakeholder roles (Admin, Producer, Veterinarian, Slaughterhouse, Consumer).")

# --- Sidebar ---
st.sidebar.success("Welcome to AgroLedger Admin Console. Navigate to other roles above.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Role Details:**")
st.sidebar.markdown("- **Admin**: Oversees total network.\n- **Producer**: Registers Sheep.\n- **Veterinarian**: Health Checks.\n- **Slaughterhouse**: Meat Processing.\n- **Consumer**: Traceability via QR.")

# --- Main Dashboard ---
st.header("Hyperledger Fabric Network Snapshot")

# 1. Top Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Registered Livestock", len(df), "+3 Today")
active_farms = df["Origin Farm"].nunique()
active_nodes = active_farms + df["Processor"].nunique() + df["Retailer"].nunique()
col2.metric("Active Network Nodes", active_nodes, "Stable")
col3.metric("Verified Health Certs", len(df[df["Health Cert"] == "Verified"]))
col4.metric("IoT Sensors Active", len(df) * 2) # e.g. Temp + GPS per sheep

st.markdown("---")

# 2. Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Livestock Distribution by Origin Farm")
    if not df.empty:
        fig_pie = px.pie(df, names="Origin Farm", hole=0.4, 
                         color_discrete_sequence=['#7C8C03', '#695D46', '#A3B18A', '#3A5A40'])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.write("No livestock registered yet.")
    
with col_chart2:
    st.subheader("Current Supply Chain Pipeline")
    if not df.empty:
        status_counts = df["Status"].value_counts().reset_index()
        fig_bar = px.bar(status_counts, x="Status", y="count", color="Status",
                         color_discrete_sequence=['#7C8C03', '#695D46', '#4CAF50'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("Pipeline is empty.")

st.markdown("---")

# 3. Network Graph (Supply Chain Flow)
st.subheader("Commodity Flow Network Visualization")
nodes = []
edges = []

if not df.empty:
    # Add Nodes
    for farm in df["Origin Farm"].dropna().unique():
        nodes.append( Node(id=farm, label=farm, size=25, color="#7C8C03") )
    for proc in df["Processor"].dropna().unique():
        nodes.append( Node(id=proc, label=proc, size=25, color="#695D46") )
    for ret in df["Retailer"].dropna().unique():
        nodes.append( Node(id=ret, label=ret, size=25, color="#A3B18A") )
        
    # Add Edges
    edge_set = set()
    for idx, row in df.iterrows():
        if pd.notna(row['Origin Farm']) and pd.notna(row['Processor']):
            edge_tuple = (row['Origin Farm'], row['Processor'])
            if edge_tuple not in edge_set:
                edges.append(Edge(source=edge_tuple[0], target=edge_tuple[1], type="CURVE_SMOOTH"))
                edge_set.add(edge_tuple)
                
        if pd.notna(row['Processor']) and pd.notna(row['Retailer']):
            edge_tuple = (row['Processor'], row['Retailer'])
            if edge_tuple not in edge_set:
                edges.append(Edge(source=edge_tuple[0], target=edge_tuple[1], type="CURVE_SMOOTH"))
                edge_set.add(edge_tuple)
        
    if nodes and edges:
        config = Config(width=1000, height=400, directed=True, physics=True, hierarchical=False)
        agraph(nodes=nodes, edges=edges, config=config)
    else:
        st.write("Not enough connected data to visualize network.")

# 4. Raw Ledger View
st.subheader("Immutable Blockchain Ledger (Admin Master View)")
st.dataframe(df, use_container_width=True)

import streamlit as st
import plotly.graph_objects as go
import datetime
import pandas as pd
from utils.blockchain_state import get_theme_css, get_ledger

st.set_page_config(page_title="AgroLedger | Consumer Verification", page_icon="🛒", layout="wide")
st.markdown(get_theme_css(), unsafe_allow_html=True)

st.title("🛒 Consumer Trust Portal")
st.markdown("*Verify the origin and ethical compliance of your food products.*")

df = get_ledger()

st.sidebar.info("Simulating a consumer scanning a QR code on a supermarket package to retrieve the item's immutable supply chain history.")
st.header("Scan Product Identity")

retail_sheep = df[df["Status"] == "At Retail"]
sample_id = retail_sheep["Sheep ID"].iloc[0] if not retail_sheep.empty else "CFS-12345"

st.write("Enter the Sheep ID found on your product packaging.")
search_id = st.text_input("🔍 Asset ID", "")
st.caption(f"Hint: Try testing with {sample_id}")

if search_id:
    result = df[df["Sheep ID"] == search_id]
    if not result.empty:
        item = result.iloc[0]
        st.success("✅ Authentic Record Found on Hyperledger Fabric Network")
        
        # Interactive Timeline
        st.subheader("Immutable Timeline")
        
        stages = ["Birth & Registration", "Processing / Abattoir", "Retail Destination"]
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
        
        # Timeline Visualization with brand colors
        fig_time = go.Figure(data=[
            go.Scatter(
                x=valid_dates, 
                y=[1]*len(valid_dates),
                mode="lines+markers+text",
                text=valid_stages,
                textposition="top center",
                hovertext=valid_entities,
                marker=dict(size=20, color="#7C8C03", line=dict(width=3, color="white")),
                line=dict(color="#695D46", width=4)
            )
        ])
        fig_time.update_layout(
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            xaxis=dict(showgrid=False),
            height=250,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig_time, use_container_width=True)
        
        st.markdown(f"**Health Certificate Origin:** {item['Health Cert']}")
        st.markdown(f"**Original Farm Coordinator:** {item['Origin Farm']}")
        st.markdown(f"**Package Location:** {item['Retailer']}")
        
        if 'event_logs' in st.session_state:
            sheep_events = [e for e in st.session_state.event_logs if e['sheep_id'] == search_id]
            if sheep_events:
                with st.expander("View Raw Blockchain Event Logs"):
                    st.json(sheep_events)
    else:
        st.error("❌ Record not found. This item cannot be verified as authentic.")

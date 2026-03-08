import streamlit as st
from utils.blockchain_state import get_theme_css, get_ledger, record_event

st.set_page_config(page_title="AgroLedger | Abattoir Operations", page_icon="🥩", layout="wide")
st.markdown(get_theme_css(), unsafe_allow_html=True)

st.title("🥩 Abattoir / Slaughterhouse")
st.markdown("*Process incoming livestock and assign packaged products to Retailers.*")

df = get_ledger()

st.sidebar.info("Slaughterhouse role: Accepts transferred sheep, processes them, and records final retail destinations.")

processors = ["Prime Cuts Ltd.", "Valley Processors", "Quality Meats"]
selected_processor = st.sidebar.selectbox("Active Processor Identity", processors)

# Filter for sheep currently at this processor
processor_data = df[(df["Processor"] == selected_processor) & (df["Status"] == "Processing")]

st.header("Incoming and Current Inventory")
if not processor_data.empty:
    st.dataframe(processor_data[["Sheep ID", "Origin Farm", "Health Cert"]], use_container_width=True)
    
    st.markdown("---")
    st.subheader("Process & Distribute Product")
    with st.form("process_form"):
        sheep_to_process = st.selectbox("Select Asset for Retail Assignment", processor_data["Sheep ID"].tolist())
        target_retailer = st.selectbox("Destined Retailer / Restaurant", ["FreshMart", "Premium Grocers", "Local Butcher", "Steakhouse 101"])
        
        process_btn = st.form_submit_button("Record Processing & Transfer")
        
        if process_btn:
             # Ensure Health Cert is verified before processing
             cert = df.loc[df["Sheep ID"] == sheep_to_process, "Health Cert"].values[0]
             if cert != "Verified":
                 st.error(f"❌ Cannot process {sheep_to_process}. Health Certificate is {cert}.")
             else:
                 df.loc[df["Sheep ID"] == sheep_to_process, "Retailer"] = target_retailer
                 df.loc[df["Sheep ID"] == sheep_to_process, "Status"] = "At Retail"
                 record_event(sheep_to_process, "Processing & Retail Distribution", f"Processed by {selected_processor}, shipped to {target_retailer}")
                 st.success(f"✅ Asset {sheep_to_process} successfully processed and assigned to {target_retailer}.")
else:
    st.info("No pending inventory to process.")

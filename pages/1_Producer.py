import streamlit as st
import datetime
import random
from utils.blockchain_state import get_theme_css, get_ledger, add_ledger_entry, record_event

st.set_page_config(page_title="AgroLedger | Producer Dashboard", page_icon="🚜", layout="wide")
st.markdown(get_theme_css(), unsafe_allow_html=True)

st.title("🚜 Producer Hub")
st.markdown("*Manage premises, register livestock, and record move-out events.*")

df = get_ledger()

# Assume we are logged in as a specific farm
farms = ["Sunrise Pastures", "Highland Sheep Co.", "Valley Farm", "Green Acres"]
selected_farm = st.sidebar.selectbox("Active Producer Profile", farms)

# Filter ledger to only show this farm's sheep
farm_data = df[df["Origin Farm"] == selected_farm]

col1, col2 = st.columns(2)
with col1:
    st.header("Register New Livestock")
    with st.form("register_form"):
        st.write("Enter birth details to mint a new digital twin on the ledger.")
        tag_id = st.text_input("New Sheep Tag ID (e.g., CFS-99999)")
        birth_date = st.date_input("Date of Birth", datetime.date.today())
        
        submitted = st.form_submit_button("Submit Registration to Blockchain")
        if submitted:
            if tag_id:
                new_sheep = {
                    "Sheep ID": tag_id,
                    "Birth Date": birth_date,
                    "Origin Farm": selected_farm,
                    "Processor": None,
                    "Retailer": None,
                    "Status": "At Farm",
                    "Health Cert": "Pending",
                    "Temperature History": [round(random.uniform(38.0, 39.5), 1)],
                    "Location Info": "Lat: 51.0, Lon: -114.0" # Mock calgary GPS
                }
                add_ledger_entry(new_sheep)
                record_event(tag_id, "Registration", f"Born at {selected_farm}")
                st.success(f"✅ Success: Asset {tag_id} registered securely.")
            else:
                st.error("Please provide a valid Tag ID.")

with col2:
    st.header("Initiate Move-Out Event")
    with st.form("move_out_form"):
        st.write("Assign sheep to transport or slaughterhouse.")
        
        available_sheep = farm_data[farm_data["Status"] == "At Farm"]["Sheep ID"].tolist()
        if available_sheep:
            selected_sheep = st.selectbox("Select Sheep to Move", available_sheep)
            destination = st.selectbox("Destination", ["Prime Cuts Ltd.", "Valley Processors", "Quality Meats"])
            transporter = st.text_input("Transporter ID / License Plate")
            move_out = st.form_submit_button("Record Movement")
            
            if move_out:
                # Update status
                df.loc[df["Sheep ID"] == selected_sheep, "Processor"] = destination
                df.loc[df["Sheep ID"] == selected_sheep, "Status"] = "Processing"
                # The state is automatically updated since we modified the df which is a ref to session state
                record_event(selected_sheep, "Move-Out", f"Sent to {destination} via {transporter}")
                st.success(f"✅ Initiated transfer of {selected_sheep} to {destination}.")
        else:
            st.info("No livestock currently 'At Farm' available for movement.")

st.markdown("---")
st.subheader("Current Active Herd")
st.dataframe(farm_data[["Sheep ID", "Birth Date", "Status", "Health Cert"]], use_container_width=True)

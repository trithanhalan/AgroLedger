import streamlit as st
from utils.blockchain_state import get_theme_css, get_ledger, record_event

st.set_page_config(page_title="AgroLedger | Veterinary Inspector", page_icon="⚕️", layout="wide")
st.markdown(get_theme_css(), unsafe_allow_html=True)

st.title("⚕️ Veterinary Inspector")
st.markdown("*Record health events and issue certificates to IPFS.*")

df = get_ledger()

st.sidebar.info("Veterinarians can view all animals to perform global health checks and issue valid clearance certificates.")

st.header("Pending Health Verifications")
# Filter for sheep that still need health checks
pending_df = df[df["Health Cert"] == "Pending"]

if not pending_df.empty:
    st.dataframe(pending_df[["Sheep ID", "Origin Farm", "Birth Date", "Status"]], use_container_width=True)
    
    st.markdown("---")
    st.subheader("Conduct Health Assessment")
    
    with st.form("health_check_form"):
        target_sheep = st.selectbox("Select Sheep to Assess", pending_df["Sheep ID"].tolist())
        health_status = st.radio("Clinical Finding", ["Cleared for Supply Chain", "Quarantine Required", "Rejected"])
        notes = st.text_area("Veterinary Notes (Will be hashed to IPFS)")
        
        submit_check = st.form_submit_button("Sign & Append to Ledger")
        
        if submit_check:
            if health_status == "Cleared for Supply Chain":
                df.loc[df["Sheep ID"] == target_sheep, "Health Cert"] = "Verified"
                st.success(f"✅ Certificate Issued: {target_sheep} is now Verified.")
                record_event(target_sheep, "Health Verification", f"Cleared by Vet. IPFS Hash: QM{hash(notes)}")
            else:
                st.warning(f"⚠️ Alert flagged for {target_sheep}: {health_status}.")
                record_event(target_sheep, "Health Alert", health_status)
else:
    st.success("All registered livestock have up-to-date health certificates!")

st.markdown("---")
st.subheader("Recent IoT Health Data (Heart Rate & Temp)")
if not df.empty:
    # Just show the first 5 for sample
    sample_iot = df.head(5)[["Sheep ID", "Temperature History", "Location Info"]]
    st.dataframe(sample_iot, use_container_width=True)

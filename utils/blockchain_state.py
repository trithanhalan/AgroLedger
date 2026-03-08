import streamlit as st
import pandas as pd
import datetime
import random

def get_theme_css():
    return ""

def init_blockchain_state():
    """Initializes the mock blockchain ledger into Streamlit's session state."""
    if 'ledger' not in st.session_state:
        # Initialize with some mock data to make the UI look populated immediately
        farms = ["Sunrise Pastures", "Highland Sheep Co."]
        processors = ["Prime Cuts Ltd.", "Valley Processors"]
        retailers = ["FreshMart", "Premium Grocers"]
        
        data = []
        for _ in range(25): # Start with 25 records
            sheep_id = f"CFS-{random.randint(10000, 99999)}"
            birth_date = datetime.date.today() - datetime.timedelta(days=random.randint(50, 400))
            farm = random.choice(farms)
            
            # Simulate supply chain progression
            progression = random.random()
            processor = random.choice(processors) if progression > 0.4 else None
            retailer = random.choice(retailers) if progression > 0.8 else None
            
            status = "At Farm"
            if retailer: status = "At Retail"
            elif processor: status = "Processing"

            data.append({
                "Sheep ID": sheep_id,
                "Birth Date": birth_date,
                "Origin Farm": farm,
                "Processor": processor,
                "Retailer": retailer,
                "Status": status,
                "Health Cert": "Verified" if random.random() > 0.2 else "Pending",
                "Temperature History": [round(random.uniform(38.0, 39.5), 1) for _ in range(5)], # Sheep normal temp is ~39
                "Location Info": f"Lat: {round(random.uniform(50.0, 55.0), 2)}, Lon: {round(random.uniform(-110.0, -90.0), 2)}"
            })
            
        st.session_state.ledger = pd.DataFrame(data)

def get_ledger():
    return st.session_state.ledger

def update_ledger(new_df):
    st.session_state.ledger = new_df

def add_ledger_entry(entry_dict):
    """Appends a new record to the ledger data frame."""
    df = st.session_state.ledger
    new_df = pd.DataFrame([entry_dict])
    st.session_state.ledger = pd.concat([new_df, df], ignore_index=True)

def record_event(sheep_id, event_type, details):
    """Simulates adding an immutable event log to the ledger for a specific sheep."""
    if 'event_logs' not in st.session_state:
         st.session_state.event_logs = []
    
    st.session_state.event_logs.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sheep_id": sheep_id,
        "event": event_type,
        "details": details
    })

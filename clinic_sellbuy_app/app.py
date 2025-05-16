import streamlit as st
import pandas as pd
import os
from datetime import date
from streamlit_extras.metric_cards import style_metric_cards

# --- SETTINGS ---
PASSWORD = "clinic123"
DATA_PATH = os.path.join("clinic_data", str(date.today()))
os.makedirs(DATA_PATH, exist_ok=True)

# --- LOGIN SCREEN ---
st.set_page_config(page_title="Clinic POS", layout="wide")
st.title("🔐 Clinic POS Login")
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd = st.text_input("Enter password", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.success("Login successful!")
    else:
        st.stop()

# --- DASHBOARD ---
st.title("📊 Clinic Dashboard")

# Simulated stats
col1, col2, col3, col4 = st.columns(4)
col1.metric("🛒 Sales", "33.6K", "↑ 4.2%")
col2.metric("📦 Purchases", "3K", "↑ 1.1%")
col3.metric("↩️ Sales Return", "429", "↓ 0.4%")
col4.metric("↪️ Purchase Return", "120", "↓ 0.2%")

style_metric_cards()

# Simulated data table
st.subheader("🧾 Sales Transactions")

data = {
    "Reference": ["SA_001", "SA_002", "SA_003"],
    "Customer": ["walk-in", "Ali", "Sara"],
    "Status": ["Completed", "Completed", "Pending"],
    "Total": [120.5, 300.0, 89.99],
    "Paid": [120.5, 300.0, 0],
    "Due": [0, 0, 89.99],
    "Payment Status": ["Paid", "Paid", "Unpaid"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

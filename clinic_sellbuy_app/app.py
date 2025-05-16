import streamlit as st
import pandas as pd
import os
from datetime import date
from streamlit_extras.metric_cards import style_metric_cards

# --- SETTINGS ---
PASSWORD = "clinic123"
DATA_PATH = os.path.join("clinic_data", str(date.today()))
os.makedirs(DATA_PATH, exist_ok=True)

# --- PAGE SETUP ---
st.set_page_config(page_title="Clinic POS", layout="wide")

# --- LOGIN SCREEN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Clinic POS Login")
    pwd = st.text_input("Enter password", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.success("Login successful!")
    else:
        st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📁 Menu")
section = st.sidebar.radio("Go to", ["Dashboard", "Sales", "Purchases", "Sales Returns", "Purchase Returns"])

st.title(f"📋 {section}")

# --- CONTENT HANDLER ---
if section == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛒 Sales", "33.6K", "↑ 4.2%")
    col2.metric("📦 Purchases", "3K", "↑ 1.1%")
    col3.metric("↩️ Sales Return", "429", "↓ 0.4%")
    col4.metric("↪️ Purchase Return", "120", "↓ 0.2%")
    style_metric_cards()

elif section == "Sales":
    st.subheader("🧾 Sales Transactions")
    data = {
        "Reference": ["SA_001", "SA_002"],
        "Customer": ["Ali", "Sara"],
        "Total": [200.0, 320.5],
        "Status": ["Completed", "Pending"],
        "Paid": [200.0, 0],
        "Due": [0, 320.5],
        "Payment Status": ["Paid", "Unpaid"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

elif section == "Purchases":
    st.subheader("📥 Purchase Entries")
    data = {
        "Invoice": ["PU_001", "PU_002"],
        "Seller": ["ABC Co", "XYZ Med"],
        "Total": [1500.0, 950.0],
        "Status": ["Received", "Pending"],
        "Paid": [1000.0, 0],
        "Due": [500.0, 950.0]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

elif section == "Sales Returns":
    st.subheader("↩️ Sales Return Records")
    st.info("No return records yet.")

elif section == "Purchase Returns":
    st.subheader("↪️ Purchase Return Records")
    st.info("No return records yet.")

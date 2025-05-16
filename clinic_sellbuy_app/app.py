import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
import zipfile

# --- SETTINGS ---
PASSWORD = "clinic123"
FOLDER_BASE = os.path.join("clinic_data", str(date.today()))

# --- LOGIN ---
st.title("🔐 Clinic Sell-Buy System")
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd = st.text_input("Enter password", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.success("Access granted.")
    else:
        st.stop()

# --- CREATE DAILY FOLDER ---
os.makedirs(FOLDER_BASE, exist_ok=True)

# --- ITEM ENTRY ---
st.header("📦 Add Item to Inventory")

with st.form("item_form"):
    name = st.text_input("Item Name")
    sell_price = st.number_input("Sell Price", min_value=0.0)
    buy_price = st.number_input("Buy Price", min_value=0.0)
    expire_date = st.date_input("Expire Date")
    barcode = st.text_input("Barcode")
    note = st.text_area("Note")
    quantity = st.number_input("Stock Quantity", min_value=0, step=1)
    submit = st.form_submit_button("💾 Save Item")

if submit:
    item = {
        "Date": datetime.now().isoformat(timespec='seconds'),
        "Name": name,
        "Sell Price": sell_price,
        "Buy Price": buy_price,
        "Expire": expire_date.isoformat(),
        "Barcode": barcode,
        "Note": note,
        "Quantity": quantity
    }
    df = pd.DataFrame([item])
    file_path = os.path.join(FOLDER_BASE, "inventory.csv")
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
    st.success("Item saved successfully!")

# --- DOWNLOAD BUTTON ---
st.markdown("### 📥 Download Today's Data")
zip_path = f"{FOLDER_BASE}.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    for root, _, files in os.walk(FOLDER_BASE):
        for file in files:
            zipf.write(os.path.join(root, file))

with open(zip_path, "rb") as file:
    st.download_button("Download ZIP", file, file_name=f"clinic_data_{date.today()}.zip")

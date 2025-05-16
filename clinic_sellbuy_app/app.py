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

# --- DASHBOARD SECTION ---
if section == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛒 Sales", "33.6K", "↑ 4.2%")
    col2.metric("📦 Purchases", "3K", "↑ 1.1%")
    col3.metric("↩️ Sales Return", "429", "↓ 0.4%")
    col4.metric("↪️ Purchase Return", "120", "↓ 0.2%")
    style_metric_cards()

# --- SALES SECTION ---
elif section == "Sales":
    st.subheader("🧾 Sales Transactions")

    # --- Add Sale Form ---
    with st.expander("➕ Add New Sale"):
        with st.form("add_sale_form"):
            customer = st.text_input("Customer Name", value="walk-in")
            barcode = st.text_input("Item Barcode")
            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            price = st.number_input("Price per Item", min_value=0.0)
            paid = st.number_input("Amount Paid", min_value=0.0)
            submit_sale = st.form_submit_button("💾 Save Sale")

        if submit_sale:
            total = quantity * price
            due = total - paid
            sale = {
                "Date": date.today().isoformat(),
                "Customer": customer,
                "Barcode": barcode,
                "Item Name": item_name,
                "Quantity": quantity,
                "Price": price,
                "Total": total,
                "Paid": paid,
                "Due": due,
                "Payment Status": "Paid" if due <= 0 else "Unpaid"
            }
            sales_path = os.path.join(DATA_PATH, "sales.csv")
            df = pd.DataFrame([sale])
            if os.path.exists(sales_path):
                df.to_csv(sales_path, mode='a', header=False, index=False)
            else:
                df.to_csv(sales_path, index=False)
            st.success("✅ Sale saved successfully!")

    # --- Show Sales Table ---
    sales_path = os.path.join(DATA_PATH, "sales.csv")
    if os.path.exists(sales_path):
        df_sales = pd.read_csv(sales_path)
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("No sales recorded today.")

# --- PURCHASES SECTION ---
elif section == "Purchases":
    st.subheader("📥 Purchase Entries")
    st.info("Purchasing form coming next...")

# --- SALES RETURN SECTION ---
elif section == "Sales Returns":
    st.subheader("↩️ Sales Return Records")
    st.info("No return records yet.")

# --- PURCHASE RETURN SECTION ---
elif section == "Purchase Returns":
    st.subheader("↪️ Purchase Return Records")
    st.info("No return records yet.")

import streamlit as st
import pandas as pd
import os
from datetime import date
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image

# --- SETTINGS ---
PASSWORD = "clinic123"
BASE_PATH = "clinic_data"
TODAY_PATH = os.path.join(BASE_PATH, str(date.today()))
INVENTORY_PATH = os.path.join(BASE_PATH, "inventory.csv")
os.makedirs(TODAY_PATH, exist_ok=True)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clinic POS", layout="wide")

# --- LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Clinic POS Login")
    pwd = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("❌ Wrong password")
    st.stop()

# --- MAIN APP ---
st.sidebar.title("📁 Menu")
section = st.sidebar.radio("Go to", ["Dashboard", "Sales", "Purchases", "Sales Returns", "Purchase Returns"])
st.title(f"📋 {section}")

# --- DASHBOARD ---
if section == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛒 Sales", "33.6K", "↑ 4.2%")
    col2.metric("📦 Purchases", "3K", "↑ 1.1%")
    col3.metric("↩️ Sales Return", "429", "↓ 0.4%")
    col4.metric("↪️ Purchase Return", "120", "↓ 0.2%")
    style_metric_cards()

# --- SALES PAGE ---
elif section == "Sales":
    st.subheader("📸 Sell Item Manually")
    image_data = st.camera_input("📷 Optional: Take a picture of the barcode")
    if image_data:
        st.info("Photo captured! Now enter the barcode manually.")
    barcode_value = st.text_input("🔢 Enter barcode number")

    item_name = ""
    price = 0.0
    if barcode_value and os.path.exists(INVENTORY_PATH):
        df_inventory = pd.read_csv(INVENTORY_PATH)
        match = df_inventory[df_inventory["Barcode"] == barcode_value]
        if not match.empty:
            item_name = match.iloc[0]["Name"]
            price = float(match.iloc[0]["Sell Price"])
            st.success(f"🧾 Found item: **{item_name}** — ${price}")
        else:
            st.warning("❌ Barcode not found in inventory")

    with st.form("sale_form_manual"):
        customer = st.text_input("Customer Name", value="walk-in")
        item = st.text_input("Item Name", value=item_name)
        quantity = st.number_input("Quantity", min_value=1, value=1)
        unit_price = st.number_input("Price per Item", value=price, format="%.2f")
        paid = st.number_input("Amount Paid", min_value=0.0)
        submit_sale = st.form_submit_button("💾 Save Sale")

    if submit_sale:
        total = quantity * unit_price
        due = total - paid
        sale = {
            "Date": date.today().isoformat(),
            "Customer": customer,
            "Barcode": barcode_value,
            "Item Name": item,
            "Quantity": quantity,
            "Price": unit_price,
            "Total": total,
            "Paid": paid,
            "Due": due,
            "Payment Status": "Paid" if due <= 0 else "Unpaid"
        }
        sales_path = os.path.join(TODAY_PATH, "sales.csv")
        df = pd.DataFrame([sale])
        if os.path.exists(sales_path):
            df.to_csv(sales_path, mode='a', header=False, index=False)
        else:
            df.to_csv(sales_path, index=False)
        st.success("✅ Sale saved successfully!")

    sales_path = os.path.join(TODAY_PATH, "sales.csv")
    if os.path.exists(sales_path):
        df_sales = pd.read_csv(sales_path)
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("No sales recorded today.")

# --- PURCHASES PAGE ---
elif section == "Purchases":
    st.subheader("🧾 Add Purchase Record")
    with st.form("purchase_form"):
        seller = st.text_input("Seller Name")
        barcode = st.text_input("Item Barcode")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1)
        unit_price = st.number_input("Buy Price per Item", min_value=0.0)
        note = st.text_area("Note (optional)")
        submit_purchase = st.form_submit_button("💾 Save Purchase")

    if submit_purchase:
        total = quantity * unit_price
        purchase = {
            "Date": date.today().isoformat(),
            "Seller": seller,
            "Barcode": barcode,
            "Item Name": item_name,
            "Quantity": quantity,
            "Price": unit_price,
            "Total": total,
            "Note": note
        }

        # Save to purchases.csv
        purchase_path = os.path.join(TODAY_PATH, "purchases.csv")
        df = pd.DataFrame([purchase])
        if os.path.exists(purchase_path):
            df.to_csv(purchase_path, mode='a', header=False, index=False)
        else:
            df.to_csv(purchase_path, index=False)

        # Update shared inventory
        if os.path.exists(INVENTORY_PATH):
            inv_df = pd.read_csv(INVENTORY_PATH)
            match = inv_df[inv_df["Barcode"] == barcode]
            if not match.empty:
                idx = match.index[0]
                inv_df.at[idx, "Quantity"] += quantity
            else:
                new_row = pd.DataFrame([{
                    "Name": item_name,
                    "Barcode": barcode,
                    "Buy Price": unit_price,
                    "Sell Price": unit_price,
                    "Quantity": quantity,
                    "Note": note
                }])
                inv_df = pd.concat([inv_df, new_row], ignore_index=True)
        else:
            inv_df = pd.DataFrame([{
                "Name": item_name,
                "Barcode": barcode,
                "Buy Price": unit_price,
                "Sell Price": unit_price,
                "Quantity": quantity,
                "Note": note
            }])
        inv_df.to_csv(INVENTORY_PATH, index=False)
        st.success("✅ Purchase saved & inventory updated!")

    purchase_path = os.path.join(TODAY_PATH, "purchases.csv")
    if os.path.exists(purchase_path):
        df_purchase = pd.read_csv(purchase_path)
        st.dataframe(df_purchase, use_container_width=True)
    else:
        st.info("No purchases recorded today.")

# --- SALES RETURNS ---
elif section == "Sales Returns":
    st.subheader("↩️ Sales Return Records")
    st.info("No return records yet.")

# --- PURCHASE RETURNS ---
elif section == "Purchase Returns":
    st.subheader("↪️ Purchase Return Records")
    st.info("No return records yet.")

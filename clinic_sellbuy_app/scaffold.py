import os

# Define the full structure
structure = {
    "": [".gitignore", "requirements.txt", "README.md", "app.py"],
    "core_platform": ["__init__.py"],
    "core_platform/accounting_module": [
        "__init__.py", "general_ledger.py", "accounts_payable.py",
        "accounts_receivable.py", "multicurrency.py", "financial_reporting.py"
    ],
    "core_platform/inventory_warehouse": [
        "__init__.py", "stock_management.py", "barcode_tracking.py",
        "batch_control.py", "warehouse_transfers.py"
    ],
    "core_platform/manufacturing": [
        "__init__.py", "bill_of_materials.py", "costing_variance.py",
        "production_planning.py"
    ],
    "core_platform/pos_restaurant": [
        "__init__.py", "pos_terminal.py", "table_management.py",
        "promotions_loyalty.py"
    ],
    "core_platform/hr_payroll": [
        "__init__.py", "employee_records.py", "attendance.py",
        "leave_advances.py", "payroll.py"
    ],
    "extensions": [],
    "extensions/pharmacy_clinic": ["__init__.py"],
    "extensions/field_sales_route_planning": ["__init__.py"],
    "extensions/retail_franchising": ["__init__.py"],
    "integrations": ["api.py", "ecommerce_connector.py", "whatsapp_module.py"],
    "compliance": ["einvoicing.py", "tax_interfaces.py", "audit_trail.py"]
}

# File templates (empty stubs with a placeholder comment)
stub_content = "# TODO: implement\n"

# Create directories and files
for folder, files in structure.items():
    # Ensure folder exists
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    # Create each file
    for filename in files:
        path = os.path.join(folder, filename) if folder else filename
        if not os.path.exists(path):
            with open(path, "w") as f:
                if filename.endswith(".py"):
                    f.write(stub_content)
                else:
                    f.write("")  # empty for .gitignore, README, etc.

print("Scaffold complete! Run `pip install -r requirements.txt` then `streamlit run app.py`.")

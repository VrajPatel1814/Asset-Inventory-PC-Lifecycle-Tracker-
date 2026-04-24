import streamlit as st
from database import add_asset, get_all_assets

def render():
    st.markdown("""
    <div class="main-header">
        <h1>➕ Add New Asset</h1>
        <p>Register a new device into the IT asset inventory</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Auto-generate next asset ID
        all_assets = get_all_assets()
        next_num   = len(all_assets) + 1
        suggested_id = f"A{str(next_num).zfill(3)}"

        with st.form("add_asset_form", clear_on_submit=True):
            st.markdown("### 🖥️ Device Information")
            col_a, col_b = st.columns(2)
            with col_a:
                asset_id    = st.text_input("Asset ID *", value=suggested_id)
                device_type = st.selectbox("Device Type *",
                    ["Laptop", "Desktop", "Monitor", "Mobile Device", "Printer",
                     "Switch", "Access Point", "Other"])
                brand       = st.text_input("Brand *", placeholder="e.g. Dell, HP, Lenovo")
                model       = st.text_input("Model *", placeholder="e.g. Latitude 5540")
            with col_b:
                serial_number = st.text_input("Serial Number *", placeholder="e.g. DL-XX1234")
                purchase_date = st.date_input("Purchase Date *")
                status        = st.selectbox("Status *",
                    ["Active", "Available", "Needs Refresh", "Retired"])

            st.markdown("### 👤 Assignment")
            col_c, col_d = st.columns(2)
            with col_c:
                assigned_to = st.text_input("Assigned To *", placeholder="Employee name or 'Unassigned'")
                department  = st.selectbox("Department *", [
                    "Finance", "HR", "IT", "Operations", "Sales",
                    "Accounting", "Engineering", "Quality", "Marketing"
                ])
            with col_d:
                location = st.selectbox("Location *", ["Windsor HQ", "Plant Floor"])
                notes    = st.text_area("Notes", placeholder="Optional notes about this device")

            submitted = st.form_submit_button("➕ Add Asset", type="primary",
                                              use_container_width=True)

        if submitted:
            if not all([asset_id, device_type, brand, model, serial_number, assigned_to]):
                st.error("Please fill in all required fields.")
            else:
                try:
                    add_asset(asset_id, device_type, brand, model, serial_number,
                              assigned_to, department, location,
                              str(purchase_date), status, notes)
                    st.success(f"✅ Asset **{asset_id}** ({brand} {model}) added successfully!")
                    st.info(f"""
                    **Asset Details:**
                    - **ID:** {asset_id} | **Type:** {device_type}
                    - **Device:** {brand} {model} (`{serial_number}`)
                    - **Assigned to:** {assigned_to} — {department} ({location})
                    - **Status:** {status}
                    """)
                except Exception as e:
                    st.error(f"Error adding asset: {e}. Asset ID or Serial Number may already exist.")

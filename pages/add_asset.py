import streamlit as st
from database import add_asset, get_all_assets

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">ASSET REGISTRY</div>
        <div class="ops-title">Register New Asset</div>
        <p class="ops-sub">Add a new device to the IT inventory system</p>
    </div>
    """, unsafe_allow_html=True)

    all_assets   = get_all_assets()
    next_num     = len(all_assets) + 1
    suggested_id = f"A{str(next_num).zfill(3)}"

    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        with st.form("add_form", clear_on_submit=True):
            st.markdown('<div class="section-label">DEVICE INFORMATION</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                asset_id    = st.text_input("ASSET ID", value=suggested_id)
                device_type = st.selectbox("DEVICE TYPE", [
                    "Laptop","Desktop","Monitor","Mobile Device",
                    "Printer","Switch","Access Point","Other"
                ])
                brand = st.text_input("BRAND", placeholder="e.g. Dell, HP, Lenovo")
                model = st.text_input("MODEL", placeholder="e.g. Latitude 5540")
            with c2:
                serial_number = st.text_input("SERIAL NUMBER", placeholder="e.g. DL-XX1234")
                purchase_date = st.date_input("PURCHASE DATE")
                status        = st.selectbox("STATUS", ["Active","Available","Needs Refresh","Retired"])

            st.markdown('<div class="section-label" style="margin-top:1rem;">ASSIGNMENT</div>',
                        unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                assigned_to = st.text_input("ASSIGNED TO", placeholder="Employee name or 'Unassigned'")
                department  = st.selectbox("DEPARTMENT", [
                    "Finance","HR","IT","Operations","Sales",
                    "Accounting","Engineering","Quality","Marketing"
                ])
            with c4:
                location = st.selectbox("LOCATION", ["Windsor HQ","Plant Floor"])
                notes    = st.text_area("NOTES", placeholder="Optional notes", height=80)

            submitted = st.form_submit_button("REGISTER ASSET →", type="primary",
                                              use_container_width=True)

        if submitted:
            if not all([asset_id, brand, model, serial_number, assigned_to]):
                st.markdown('<div class="alert-bar">✗ ALL FIELDS ARE REQUIRED</div>',
                            unsafe_allow_html=True)
            else:
                try:
                    add_asset(asset_id, device_type, brand, model, serial_number,
                              assigned_to, department, location, str(purchase_date), status, notes)
                    st.markdown(f"""
                    <div class="ok-bar">
                        ✓ ASSET REGISTERED — {asset_id} · {brand} {model}<br>
                        SERIAL: {serial_number} · {department} · {location} · {status}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="alert-bar">✗ ERROR: {e} — Asset ID or Serial may already exist.</div>',
                                unsafe_allow_html=True)

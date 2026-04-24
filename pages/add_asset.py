import streamlit as st
from database import add_asset, get_all_assets
from theme import THEME_CSS

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">➕</div>
        <div class="page-header-text">
            <div class="eyebrow">Asset Registry</div>
            <h1>Add New Asset</h1>
            <p>Register a new device into the IT inventory system</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    all_assets   = get_all_assets()
    suggested_id = f"A{str(len(all_assets)+1).zfill(3)}"

    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        with st.form("add_form", clear_on_submit=True):
            st.markdown('<div class="section-head">Device Information</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                asset_id    = st.text_input("Asset ID", value=suggested_id)
                device_type = st.selectbox("Device Type", [
                    "Laptop","Desktop","Monitor","Mobile Device",
                    "Printer","Switch","Access Point","Other"
                ])
                brand = st.text_input("Brand", placeholder="e.g. Dell, HP, Lenovo")
                model = st.text_input("Model", placeholder="e.g. Latitude 5540")
            with c2:
                serial  = st.text_input("Serial Number", placeholder="e.g. DL-XX1234")
                pdate   = st.date_input("Purchase Date")
                status  = st.selectbox("Status", ["Active","Available","Needs Refresh","Retired"])

            st.markdown('<div class="section-head" style="margin-top:1rem;">Assignment</div>',
                        unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                assigned = st.text_input("Assigned To", placeholder="Employee name or 'Unassigned'")
                dept     = st.selectbox("Department", [
                    "Finance","HR","IT","Operations","Sales",
                    "Accounting","Engineering","Quality","Marketing"
                ])
            with c4:
                location = st.selectbox("Location", ["Windsor HQ","Plant Floor"])
                notes    = st.text_area("Notes", placeholder="Optional notes", height=80)

            sub = st.form_submit_button("Register Asset →", type="primary",
                                         use_container_width=True)

        if sub:
            if not all([asset_id, brand, model, serial, assigned]):
                st.markdown('<div class="alert-pill">⚠️ &nbsp; All fields are required</div>',
                            unsafe_allow_html=True)
            else:
                try:
                    add_asset(asset_id, device_type, brand, model, serial,
                              assigned, dept, location, str(pdate), status, notes)
                    st.markdown(f"""
                    <div class="ok-pill" style="display:block;border-radius:10px;padding:1rem 1.2rem;">
                        ✅ &nbsp; <b>{asset_id} registered successfully</b><br>
                        <span style="font-size:0.82rem;margin-left:1.6rem;">
                            {brand} {model} · {device_type}<br>
                            Assigned to: {assigned} · {dept} · {location}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="alert-pill">⚠️ &nbsp; Error: {e}</div>',
                                unsafe_allow_html=True)

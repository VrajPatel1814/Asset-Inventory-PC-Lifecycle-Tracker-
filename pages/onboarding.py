import streamlit as st
from database import get_all_assets, log_onboarding, update_asset

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">EMPLOYEE LIFECYCLE</div>
        <div class="ops-title">Equipment Onboarding</div>
        <p class="ops-sub">Assign IT equipment to a new employee and log the transition</p>
    </div>
    """, unsafe_allow_html=True)

    available = [a for a in get_all_assets(status_filter="Available")]

    if not available:
        st.markdown("""
        <div class="warn-bar">
            ⚠ NO AVAILABLE ASSETS — All devices are currently assigned or retired.
            Offboard an employee or retire a device to free up inventory.
        </div>
        """, unsafe_allow_html=True)
        return

    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown(f"""
        <div class="ok-bar">
            ✓ {len(available)} ASSETS AVAILABLE FOR ASSIGNMENT
        </div>
        """, unsafe_allow_html=True)

        with st.form("onboarding_form", clear_on_submit=True):
            st.markdown('<div class="section-label">EMPLOYEE DETAILS</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                employee_name = st.text_input("FULL NAME", placeholder="e.g. John Smith")
                department    = st.selectbox("DEPARTMENT", [
                    "Finance","HR","IT","Operations","Sales",
                    "Accounting","Engineering","Quality","Marketing"
                ])
            with c2:
                location     = st.selectbox("LOCATION", ["Windsor HQ","Plant Floor"])
                processed_by = st.text_input("PROCESSED BY (IT STAFF)",
                                             placeholder="e.g. Omar Farouk")

            st.markdown('<div class="section-label" style="margin-top:1rem;">SELECT EQUIPMENT TO ASSIGN</div>',
                        unsafe_allow_html=True)

            asset_options = {
                f"{a['asset_id']}  ·  {a['brand']} {a['model']}  ·  {a['device_type']}": a["asset_id"]
                for a in available
            }

            selected_labels = st.multiselect(
                "AVAILABLE ASSETS", options=list(asset_options.keys()),
                help="Only Available assets are shown"
            )

            notes = st.text_area("NOTES", placeholder="e.g. Standard kit for Finance — laptop + monitor",
                                 height=80)

            submitted = st.form_submit_button("COMPLETE ONBOARDING →",
                                             type="primary", use_container_width=True)

        if submitted:
            if not employee_name or not processed_by or not selected_labels:
                st.markdown('<div class="alert-bar">✗ MISSING REQUIRED FIELDS — name, IT staff, and at least one asset</div>',
                            unsafe_allow_html=True)
            else:
                selected_ids = [asset_options[l] for l in selected_labels]
                for aid in selected_ids:
                    update_asset(aid, employee_name, department, location, "Active", "", processed_by)
                log_onboarding(employee_name, department, selected_ids, processed_by, notes)

                st.markdown(f"""
                <div class="ok-bar">
                    ✓ ONBOARDING COMPLETE — {employee_name} · {department} · {location}<br>
                    ASSETS ASSIGNED: {', '.join(selected_ids)}<br>
                    PROCESSED BY: {processed_by} · LOGGED TO TRANSITION RECORD
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

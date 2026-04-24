import streamlit as st
from database import get_all_employees, get_assets_by_employee, log_offboarding

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">EMPLOYEE LIFECYCLE</div>
        <div class="ops-title">Equipment Offboarding</div>
        <p class="ops-sub">Collect and return IT equipment from departing or transferring employees</p>
    </div>
    """, unsafe_allow_html=True)

    employees  = get_all_employees()
    emp_names  = [e["name"] for e in employees]

    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        selected = st.selectbox("SELECT EMPLOYEE", ["— SELECT EMPLOYEE —"] + emp_names)

        if selected and selected != "— SELECT EMPLOYEE —":
            emp_info   = next((e for e in employees if e["name"] == selected), None)
            emp_assets = get_assets_by_employee(selected)

            if emp_info:
                st.markdown(f"""
                <div style="background:#141720; border:1px solid #2a2f3d; border-radius:4px;
                            padding:0.7rem 1rem; margin-bottom:1rem;
                            font-family:IBM Plex Mono,monospace; font-size:0.75rem; color:#94a3b8;">
                    EMPLOYEE: <span style="color:#e2e8f0;">{selected}</span>
                    &nbsp;·&nbsp; DEPT: <span style="color:#e2e8f0;">{emp_info['department']}</span>
                    &nbsp;·&nbsp; LOCATION: <span style="color:#e2e8f0;">{emp_info['location']}</span>
                </div>
                """, unsafe_allow_html=True)

            if not emp_assets:
                st.markdown('<div class="warn-bar">⚠ NO ACTIVE ASSETS ASSIGNED TO THIS EMPLOYEE</div>',
                            unsafe_allow_html=True)
                return

            st.markdown(f'<div class="section-label">CURRENTLY ASSIGNED — {len(emp_assets)} ITEMS</div>',
                        unsafe_allow_html=True)
            for a in emp_assets:
                st.markdown(f"""
                <div class="asset-row">
                    <span class="mono-tag">{a['asset_id']}</span>
                    &nbsp; <span style="color:#e2e8f0;font-size:0.85rem;">{a['brand']} {a['model']}</span>
                    &nbsp; <span style="color:#64748b;font-size:0.8rem;">· {a['device_type']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            asset_options = {
                f"{a['asset_id']}  ·  {a['brand']} {a['model']}": a["asset_id"]
                for a in emp_assets
            }

            with st.form("offboarding_form", clear_on_submit=True):
                st.markdown('<div class="section-label">SELECT ASSETS BEING RETURNED</div>',
                            unsafe_allow_html=True)
                returned = st.multiselect("RETURNING ASSETS",
                    options=list(asset_options.keys()),
                    default=list(asset_options.keys()))
                c1, c2 = st.columns(2)
                with c1:
                    processed_by = st.text_input("PROCESSED BY (IT STAFF)",
                                                 placeholder="e.g. Fatima Al-Hassan")
                with c2:
                    notes = st.text_area("NOTES", height=80,
                                         placeholder="e.g. All equipment returned in good condition")

                submitted = st.form_submit_button("COMPLETE OFFBOARDING →",
                                                  type="primary", use_container_width=True)

            if submitted:
                if not processed_by or not returned:
                    st.markdown('<div class="alert-bar">✗ SELECT AT LEAST ONE ASSET AND ENTER IT STAFF NAME</div>',
                                unsafe_allow_html=True)
                else:
                    returned_ids = [asset_options[l] for l in returned]
                    dept = emp_info["department"] if emp_info else "Unknown"
                    log_offboarding(selected, dept, returned_ids, processed_by, notes)

                    st.markdown(f"""
                    <div class="ok-bar">
                        ✓ OFFBOARDING COMPLETE — {selected}<br>
                        ASSETS RETURNED: {', '.join(returned_ids)} → STATUS: AVAILABLE<br>
                        PROCESSED BY: {processed_by} · LOGGED TO TRANSITION RECORD
                    </div>
                    """, unsafe_allow_html=True)

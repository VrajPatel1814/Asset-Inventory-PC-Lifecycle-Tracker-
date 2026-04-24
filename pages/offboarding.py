import streamlit as st
from database import get_all_employees, get_assets_by_employee, log_offboarding
from theme import THEME_CSS

TYPE_ICONS = {"Laptop":"💻","Desktop":"🖥️","Monitor":"🖵","Mobile Device":"📱"}

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🚪</div>
        <div class="page-header-text">
            <div class="eyebrow">Workforce</div>
            <h1>Employee Offboarding</h1>
            <p>Collect and return IT equipment from departing or transferring employees</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    employees = get_all_employees()
    emp_names = [e["name"] for e in employees]

    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        selected = st.selectbox("Select Employee", ["— Select an employee —"] + emp_names)

        if selected and selected != "— Select an employee —":
            emp_info   = next((e for e in employees if e["name"] == selected), None)
            emp_assets = get_assets_by_employee(selected)

            if emp_info:
                st.markdown(f"""
                <div class="info-row">
                    👤 &nbsp; <b>{selected}</b> &nbsp;·&nbsp;
                    {emp_info['department']} &nbsp;·&nbsp;
                    {emp_info['location']}
                </div>
                """, unsafe_allow_html=True)

            if not emp_assets:
                st.markdown('<div class="warn-pill">⚠️ &nbsp; No active assets assigned to this employee</div>',
                            unsafe_allow_html=True)
                return

            st.markdown(f'<div class="section-head">Currently Assigned — {len(emp_assets)} Items</div>',
                        unsafe_allow_html=True)
            for a in emp_assets:
                icon = TYPE_ICONS.get(a["device_type"],"🔧")
                st.markdown(f"""
                <div class="asset-card" style="display:flex;align-items:center;gap:10px;">
                    <span style="font-size:1.2rem;">{icon}</span>
                    <div>
                        <span style="font-weight:600;font-size:0.9rem;">{a['brand']} {a['model']}</span>
                        <span style="color:#6b7c6e;font-size:0.8rem;margin-left:8px;">{a['device_type']}</span><br>
                        <span class="mono" style="font-size:0.75rem;color:#52b788;">{a['asset_id']}</span>
                        <span style="color:#6b7c6e;font-size:0.75rem;margin-left:6px;">· {a['serial_number']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            opts = {
                f"{a['asset_id']}  ·  {a['brand']} {a['model']}": a["asset_id"]
                for a in emp_assets
            }

            with st.form("offboarding_form", clear_on_submit=True):
                st.markdown('<div class="section-head">Assets Being Returned</div>',
                            unsafe_allow_html=True)
                returned = st.multiselect("Select returning assets",
                    options=list(opts.keys()), default=list(opts.keys()))
                c1, c2 = st.columns(2)
                with c1:
                    by    = st.text_input("Processed By (IT Staff)", placeholder="e.g. Fatima Al-Hassan")
                with c2:
                    notes = st.text_area("Notes", height=80,
                                         placeholder="e.g. All equipment returned in good condition")

                sub = st.form_submit_button("Complete Offboarding →",
                                             type="primary", use_container_width=True)

            if sub:
                if not by or not returned:
                    st.markdown('<div class="alert-pill">⚠️ &nbsp; Select at least one asset and enter IT staff name</div>',
                                unsafe_allow_html=True)
                else:
                    ids  = [opts[l] for l in returned]
                    dept = emp_info["department"] if emp_info else "Unknown"
                    log_offboarding(selected, dept, ids, by, notes)
                    st.markdown(f"""
                    <div class="ok-pill" style="display:block;border-radius:10px;padding:1rem 1.2rem;">
                        ✅ &nbsp; <b>Offboarding complete for {selected}</b><br>
                        <span style="font-size:0.82rem;margin-left:1.6rem;">
                            Assets returned: {', '.join(ids)} → Status: Available<br>
                            Processed by: {by}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

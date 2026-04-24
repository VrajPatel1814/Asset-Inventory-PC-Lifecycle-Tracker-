import streamlit as st
from database import get_all_assets, log_onboarding, update_asset
from theme import THEME_CSS

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">👋</div>
        <div class="page-header-text">
            <div class="eyebrow">Workforce</div>
            <h1>Employee Onboarding</h1>
            <p>Assign IT equipment to a new employee and generate a transition record</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    available = [a for a in get_all_assets(status_filter="Available")]

    if not available:
        st.markdown("""
        <div class="warn-pill">
            ⚠️ &nbsp; No available assets right now.
            Offboard an employee or add new equipment to free up inventory.
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f'<div class="ok-pill">✅ &nbsp; {len(available)} assets available for assignment</div>',
                unsafe_allow_html=True)

    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        with st.form("onboarding_form", clear_on_submit=True):
            st.markdown('<div class="section-head">Employee Details</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                name  = st.text_input("Full Name", placeholder="e.g. John Smith")
                dept  = st.selectbox("Department", [
                    "Finance","HR","IT","Operations","Sales",
                    "Accounting","Engineering","Quality","Marketing"
                ])
            with c2:
                loc   = st.selectbox("Location", ["Windsor HQ","Plant Floor"])
                by    = st.text_input("Processed By (IT Staff)", placeholder="e.g. Omar Farouk")

            st.markdown('<div class="section-head" style="margin-top:1rem;">Equipment to Assign</div>',
                        unsafe_allow_html=True)

            opts = {
                f"{a['asset_id']}  ·  {a['brand']} {a['model']}  ({a['device_type']})": a["asset_id"]
                for a in available
            }
            chosen = st.multiselect("Select assets", options=list(opts.keys()),
                                    help="Only Available assets are shown")
            notes  = st.text_area("Notes", placeholder="e.g. Standard Finance kit — laptop + monitor",
                                  height=80)

            sub = st.form_submit_button("Complete Onboarding →", type="primary",
                                        use_container_width=True)

        if sub:
            if not name or not by or not chosen:
                st.markdown('<div class="alert-pill">⚠️ &nbsp; Please fill in all required fields and select at least one asset</div>',
                            unsafe_allow_html=True)
            else:
                ids = [opts[l] for l in chosen]
                for aid in ids:
                    update_asset(aid, name, dept, loc, "Active", "", by)
                log_onboarding(name, dept, ids, by, notes)

                st.markdown(f"""
                <div class="ok-pill" style="display:block;border-radius:10px;padding:1rem 1.2rem;">
                    ✅ &nbsp; <b>Onboarding complete for {name}</b><br>
                    <span style="font-size:0.82rem;margin-left:1.6rem;">
                        Department: {dept} · {loc}<br>
                        Assets assigned: {', '.join(ids)}<br>
                        Processed by: {by}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

import streamlit as st
import pandas as pd
from database import get_all_assets, get_asset_by_id, update_asset, retire_asset
from theme import THEME_CSS

BADGE_HTML = {
    "Active":        '<span class="badge b-active">Active</span>',
    "Needs Refresh": '<span class="badge b-refresh">Needs Refresh</span>',
    "Retired":       '<span class="badge b-retired">Retired</span>',
    "Available":     '<span class="badge b-available">Available</span>',
}

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🗂️</div>
        <div class="page-header-text">
            <div class="eyebrow">Asset Registry</div>
            <h1>Asset Inventory</h1>
            <p>Search, filter and manage every tracked IT device</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FILTERS ──────────────────────────────────────────────────
    with st.container():
        fc = st.columns(5)
        sf  = fc[0].selectbox("Status",   ["All","Active","Needs Refresh","Retired","Available"])
        df_ = fc[1].selectbox("Dept",     ["All","Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"])
        tf  = fc[2].selectbox("Type",     ["All","Laptop","Desktop","Monitor","Mobile Device"])
        lf  = fc[3].selectbox("Location", ["All","Windsor HQ","Plant Floor"])
        kw  = fc[4].text_input("Search", placeholder="name, serial, model…")

    assets = get_all_assets(
        status_filter=None   if sf  == "All" else sf,
        dept_filter=None     if df_ == "All" else df_,
        type_filter=None     if tf  == "All" else tf,
        location_filter=None if lf  == "All" else lf,
    )
    if kw:
        s = kw.lower()
        assets = [a for a in assets if s in a["asset_id"].lower() or
                  s in a["serial_number"].lower() or s in a["assigned_to"].lower() or
                  s in a["model"].lower() or s in a["brand"].lower()]

    row_l, row_r = st.columns([3,1])
    row_l.markdown(f'<p style="color:#6b7c6e;font-size:0.82rem;margin:0.5rem 0;">'
                   f'Showing <b style="color:#2d6a4f">{len(assets)}</b> assets</p>',
                   unsafe_allow_html=True)
    if assets:
        with row_r:
            csv = pd.DataFrame([dict(a) for a in assets]).to_csv(index=False).encode()
            st.download_button("⬇ Export CSV", csv, "assets.csv", "text/csv",
                               use_container_width=True)

    st.markdown('<hr style="border:none;border-top:1.5px solid #e2e8da;margin:0.5rem 0 1rem;">', unsafe_allow_html=True)

    if not assets:
        st.markdown('<div class="warn-pill">⚠️ &nbsp; No assets match the selected filters</div>',
                    unsafe_allow_html=True)
        return

    # ── TABLE HEADER ─────────────────────────────────────────────
    hc = st.columns([0.8,1.1,1.8,1.5,2,1.4,1.3,1.3,0.5])
    for col, label in zip(hc, ["ID","Type","Device","Serial","Assigned To","Dept","Location","Status",""]):
        col.markdown(f'<span class="tbl-col-head">{label}</span>', unsafe_allow_html=True)
    st.markdown('<hr style="border:none;border-top:1.5px solid #e2e8da;margin:0.3rem 0 0.5rem;">', unsafe_allow_html=True)

    if "edit_asset" not in st.session_state:
        st.session_state.edit_asset = None

    TYPE_ICONS = {"Laptop":"💻","Desktop":"🖥️","Monitor":"🖵","Mobile Device":"📱"}

    for asset in assets:
        badge = BADGE_HTML.get(asset["status"],"")
        icon  = TYPE_ICONS.get(asset["device_type"],"🔧")
        rc    = st.columns([0.8,1.1,1.8,1.5,2,1.4,1.3,1.3,0.5])
        rc[0].markdown(f'<span class="mono" style="color:#2d6a4f;font-weight:600;">{asset["asset_id"]}</span>', unsafe_allow_html=True)
        rc[1].markdown(f'<span style="font-size:0.85rem;">{icon} {asset["device_type"]}</span>', unsafe_allow_html=True)
        rc[2].markdown(f'<span style="font-size:0.85rem;font-weight:500;">{asset["brand"]} {asset["model"]}</span>', unsafe_allow_html=True)
        rc[3].markdown(f'<span class="mono" style="color:#6b7c6e;">{asset["serial_number"]}</span>', unsafe_allow_html=True)
        rc[4].markdown(f'<span style="font-size:0.85rem;">{asset["assigned_to"]}</span>', unsafe_allow_html=True)
        rc[5].markdown(f'<span style="font-size:0.82rem;color:#6b7c6e;">{asset["department"]}</span>', unsafe_allow_html=True)
        rc[6].markdown(f'<span style="font-size:0.82rem;color:#6b7c6e;">{asset["location"]}</span>', unsafe_allow_html=True)
        rc[7].markdown(badge, unsafe_allow_html=True)
        if rc[8].button("✏️", key=f"e_{asset['asset_id']}"):
            st.session_state.edit_asset = asset["asset_id"]
            st.rerun()
        st.markdown('<hr style="border:none;border-top:1px solid #f4f6f3;margin:2px 0;">', unsafe_allow_html=True)

    # ── EDIT PANEL ────────────────────────────────────────────────
    if st.session_state.edit_asset:
        asset = get_asset_by_id(st.session_state.edit_asset)
        if asset:
            st.markdown(f"""
            <div class="edit-panel">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">
                    <div style="background:#d8f3dc;border-radius:8px;padding:8px;font-size:1.2rem;">✏️</div>
                    <div>
                        <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                                    letter-spacing:0.1em;color:#52b788;">Editing Record</div>
                        <div style="font-size:1rem;font-weight:700;color:#1a2e1d;">
                            {asset['asset_id']} &nbsp;·&nbsp; {asset['brand']} {asset['model']}
                            <span class="mono" style="font-size:0.78rem;color:#6b7c6e;
                                  background:#f4f6f3;padding:2px 8px;border-radius:4px;margin-left:6px;">
                                {asset['serial_number']}
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                new_assigned = st.text_input("Assigned To", value=asset["assigned_to"])
                depts = ["Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"]
                new_dept = st.selectbox("Department", depts,
                    index=depts.index(asset["department"]) if asset["department"] in depts else 0)
                new_notes = st.text_area("Notes", value=asset["notes"] or "", height=80)
            with c2:
                new_loc = st.selectbox("Location", ["Windsor HQ","Plant Floor"],
                    index=["Windsor HQ","Plant Floor"].index(asset["location"])
                          if asset["location"] in ["Windsor HQ","Plant Floor"] else 0)
                statuses = ["Active","Needs Refresh","Retired","Available"]
                new_status = st.selectbox("Status", statuses,
                    index=statuses.index(asset["status"]) if asset["status"] in statuses else 0)
                st.markdown(f'<p style="font-size:0.8rem;color:#6b7c6e;margin-top:0.5rem;">Purchase date: <b>{asset["purchase_date"]}</b></p>', unsafe_allow_html=True)

            bc1, bc2, bc3 = st.columns(3)
            with bc1:
                if st.button("Save Changes", type="primary", use_container_width=True):
                    update_asset(asset["asset_id"], new_assigned, new_dept,
                                 new_loc, new_status, new_notes, "IT Admin")
                    st.markdown('<div class="ok-pill">✅ &nbsp; Record updated successfully</div>', unsafe_allow_html=True)
                    st.session_state.edit_asset = None
                    st.rerun()
            with bc2:
                if st.button("Retire Asset", use_container_width=True):
                    retire_asset(asset["asset_id"], "IT Admin")
                    st.markdown('<div class="warn-pill">📦 &nbsp; Asset retired</div>', unsafe_allow_html=True)
                    st.session_state.edit_asset = None
                    st.rerun()
            with bc3:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.edit_asset = None
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

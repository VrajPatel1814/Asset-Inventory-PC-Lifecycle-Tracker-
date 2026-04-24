import streamlit as st
import pandas as pd
from database import get_all_assets, get_asset_by_id, update_asset, retire_asset

BADGE = {
    "Active":        '<span class="badge b-active">ACTIVE</span>',
    "Needs Refresh": '<span class="badge b-refresh">REFRESH</span>',
    "Retired":       '<span class="badge b-retired">RETIRED</span>',
    "Available":     '<span class="badge b-available">AVAILABLE</span>',
}

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">ASSET REGISTRY</div>
        <div class="ops-title">Asset Inventory</div>
        <p class="ops-sub">Search, filter and manage all tracked IT devices</p>
    </div>
    """, unsafe_allow_html=True)

    # ── FILTERS ──────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: sf = st.selectbox("STATUS",   ["All","Active","Needs Refresh","Retired","Available"], label_visibility="visible")
    with c2: df_f = st.selectbox("DEPT",   ["All","Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"])
    with c3: tf = st.selectbox("TYPE",     ["All","Laptop","Desktop","Monitor","Mobile Device"])
    with c4: lf = st.selectbox("LOCATION", ["All","Windsor HQ","Plant Floor"])
    with c5: kw = st.text_input("SEARCH", placeholder="asset ID, name, model...")

    assets = get_all_assets(
        status_filter=None   if sf   == "All" else sf,
        dept_filter=None     if df_f == "All" else df_f,
        type_filter=None     if tf   == "All" else tf,
        location_filter=None if lf   == "All" else lf,
    )
    if kw:
        s = kw.lower()
        assets = [a for a in assets if s in a["asset_id"].lower() or
                  s in a["serial_number"].lower() or s in a["assigned_to"].lower() or
                  s in a["model"].lower() or s in a["brand"].lower()]

    col_l, col_r = st.columns([3,1])
    with col_l:
        st.markdown(f'<span style="font-family:IBM Plex Mono,monospace; font-size:0.75rem; color:#64748b;">'
                    f'{len(assets)} RECORDS FOUND</span>', unsafe_allow_html=True)
    with col_r:
        if assets:
            csv = pd.DataFrame([dict(a) for a in assets]).to_csv(index=False).encode()
            st.download_button("⬇ EXPORT CSV", csv, "assets.csv", "text/csv",
                               use_container_width=True)

    st.markdown('<hr style="border-color:#2a2f3d; margin:0.8rem 0;">', unsafe_allow_html=True)

    if not assets:
        st.markdown('<div class="warn-bar">NO ASSETS MATCH THE SELECTED FILTERS</div>',
                    unsafe_allow_html=True)
        return

    # ── TABLE HEADER ──────────────────────────────────────────────
    st.markdown("""
    <div class="tbl-header">
        <div style="display:grid; grid-template-columns:0.7fr 1fr 1.6fr 1.4fr 1.8fr 1.3fr 1.2fr 1.1fr 0.5fr;
                    gap:0.5rem; align-items:center;">
            <span>ID</span><span>TYPE</span><span>DEVICE</span><span>SERIAL</span>
            <span>ASSIGNED TO</span><span>DEPT</span><span>LOCATION</span><span>STATUS</span><span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "edit_asset" not in st.session_state:
        st.session_state.edit_asset = None

    for asset in assets:
        badge = BADGE.get(asset["status"], "")
        c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([0.7,1,1.6,1.4,1.8,1.3,1.2,1.1,0.5])
        c1.markdown(f'<span class="mono-tag">{asset["asset_id"]}</span>', unsafe_allow_html=True)
        c2.markdown(f'<small style="color:#94a3b8">{asset["device_type"]}</small>', unsafe_allow_html=True)
        c3.markdown(f'<span style="color:#e2e8f0;font-size:0.85rem">{asset["brand"]} {asset["model"]}</span>', unsafe_allow_html=True)
        c4.markdown(f'<span class="mono-tag">{asset["serial_number"]}</span>', unsafe_allow_html=True)
        c5.markdown(f'<span style="color:#e2e8f0;font-size:0.85rem">{asset["assigned_to"]}</span>', unsafe_allow_html=True)
        c6.markdown(f'<small style="color:#64748b">{asset["department"]}</small>', unsafe_allow_html=True)
        c7.markdown(f'<small style="color:#64748b">{asset["location"]}</small>', unsafe_allow_html=True)
        c8.markdown(badge, unsafe_allow_html=True)
        if c9.button("✎", key=f"e_{asset['asset_id']}"):
            st.session_state.edit_asset = asset["asset_id"]
            st.rerun()
        st.markdown('<hr style="border-color:#1c2030;margin:2px 0;">', unsafe_allow_html=True)

    # ── EDIT PANEL ────────────────────────────────────────────────
    if st.session_state.edit_asset:
        asset = get_asset_by_id(st.session_state.edit_asset)
        if asset:
            st.markdown(f"""
            <div style="background:#141720; border:1px solid #f59e0b; border-radius:6px;
                        padding:1.2rem 1.4rem; margin-top:1rem;">
                <div class="ops-tag">EDITING RECORD</div>
                <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0; margin-bottom:0.8rem;">
                    {asset['asset_id']} · {asset['brand']} {asset['model']}
                    <span class="mono-tag" style="margin-left:8px;">{asset['serial_number']}</span>
                </div>
            """, unsafe_allow_html=True)

            c1,c2 = st.columns(2)
            with c1:
                st.caption(f"Purchase Date: {asset['purchase_date']}")
                new_assigned = st.text_input("ASSIGNED TO", value=asset["assigned_to"])
                depts = ["Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"]
                new_dept = st.selectbox("DEPARTMENT", depts,
                    index=depts.index(asset["department"]) if asset["department"] in depts else 0)
            with c2:
                new_loc = st.selectbox("LOCATION", ["Windsor HQ","Plant Floor"],
                    index=["Windsor HQ","Plant Floor"].index(asset["location"])
                          if asset["location"] in ["Windsor HQ","Plant Floor"] else 0)
                statuses = ["Active","Needs Refresh","Retired","Available"]
                new_status = st.selectbox("STATUS", statuses,
                    index=statuses.index(asset["status"]) if asset["status"] in statuses else 0)
                new_notes = st.text_area("NOTES", value=asset["notes"] or "", height=80)

            cs, cr, cc = st.columns(3)
            with cs:
                if st.button("SAVE CHANGES", type="primary", use_container_width=True):
                    update_asset(asset["asset_id"], new_assigned, new_dept,
                                 new_loc, new_status, new_notes, "IT Admin")
                    st.markdown('<div class="ok-bar">✓ RECORD UPDATED SUCCESSFULLY</div>',
                                unsafe_allow_html=True)
                    st.session_state.edit_asset = None
                    st.rerun()
            with cr:
                if st.button("RETIRE ASSET", use_container_width=True):
                    retire_asset(asset["asset_id"], "IT Admin")
                    st.markdown('<div class="warn-bar">⚠ ASSET RETIRED</div>',
                                unsafe_allow_html=True)
                    st.session_state.edit_asset = None
                    st.rerun()
            with cc:
                if st.button("CANCEL", use_container_width=True):
                    st.session_state.edit_asset = None
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

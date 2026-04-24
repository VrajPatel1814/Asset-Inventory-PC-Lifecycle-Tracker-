import streamlit as st
import pandas as pd
from database import get_all_assets, get_asset_by_id, update_asset, retire_asset

def render():
    st.markdown("""
    <div class="main-header">
        <h1>🖥️ Asset Inventory</h1>
        <p>Search, filter, and manage all 75+ IT assets</p>
    </div>
    """, unsafe_allow_html=True)

    # ── FILTERS ──────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: status_f   = st.selectbox("Status",   ["All","Active","Needs Refresh","Retired","Available"])
    with col2: dept_f     = st.selectbox("Department",["All","Finance","HR","IT","Operations","Sales",
                                                        "Accounting","Engineering","Quality","Marketing"])
    with col3: type_f     = st.selectbox("Type",     ["All","Laptop","Desktop","Monitor","Mobile Device"])
    with col4: location_f = st.selectbox("Location", ["All","Windsor HQ","Plant Floor"])
    with col5: search     = st.text_input("🔍 Search", placeholder="Name, serial, model...")

    assets = get_all_assets(
        status_filter=None   if status_f   == "All" else status_f,
        dept_filter=None     if dept_f     == "All" else dept_f,
        type_filter=None     if type_f     == "All" else type_f,
        location_filter=None if location_f == "All" else location_f,
    )

    if search:
        s = search.lower()
        assets = [a for a in assets if
                  s in a["asset_id"].lower() or
                  s in a["serial_number"].lower() or
                  s in a["assigned_to"].lower() or
                  s in a["model"].lower() or
                  s in a["brand"].lower()]

    st.markdown(f"**{len(assets)} asset(s) found**")

    # ── EXPORT CSV ───────────────────────────────────────────────
    if assets:
        df_export = pd.DataFrame([dict(a) for a in assets])
        csv = df_export.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export to CSV", csv, "assets_export.csv",
                           "text/csv", use_container_width=False)

    st.markdown("---")

    if not assets:
        st.info("No assets match the selected filters.")
        return

    STATUS_ICON = {"Active":"🟢","Needs Refresh":"🟡","Retired":"⚫","Available":"🔵"}

    if "edit_asset" not in st.session_state:
        st.session_state.edit_asset = None

    # ── ASSET TABLE ───────────────────────────────────────────────
    header = st.columns([1, 1.2, 1.5, 1.5, 1.8, 1.5, 1.2, 1.2, 0.8])
    for col, label in zip(header, ["ID","Type","Brand / Model","Serial #",
                                    "Assigned To","Department","Location","Status",""]):
        col.markdown(f"**{label}**")
    st.divider()

    for asset in assets:
        icon = STATUS_ICON.get(asset["status"], "⚪")
        cols = st.columns([1, 1.2, 1.5, 1.5, 1.8, 1.5, 1.2, 1.2, 0.8])
        cols[0].markdown(asset["asset_id"])
        cols[1].markdown(asset["device_type"])
        cols[2].markdown(f"{asset['brand']} {asset['model']}")
        cols[3].markdown(f"`{asset['serial_number']}`")
        cols[4].markdown(asset["assigned_to"])
        cols[5].markdown(asset["department"])
        cols[6].markdown(asset["location"])
        cols[7].markdown(f"{icon} {asset['status']}")
        if cols[8].button("✏️", key=f"edit_{asset['asset_id']}"):
            st.session_state.edit_asset = asset["asset_id"]
            st.rerun()
        st.divider()

    # ── EDIT PANEL ────────────────────────────────────────────────
    if st.session_state.edit_asset:
        asset = get_asset_by_id(st.session_state.edit_asset)
        if asset:
            st.markdown("---")
            st.markdown(f"### ✏️ Editing: {asset['asset_id']} — {asset['brand']} {asset['model']}")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Serial Number:** `{asset['serial_number']}`")
                st.markdown(f"**Purchase Date:** {asset['purchase_date']}")
                new_assigned = st.text_input("Assigned To", value=asset["assigned_to"])
                new_dept     = st.selectbox("Department",
                    ["Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"],
                    index=["Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"].index(
                        asset["department"]) if asset["department"] in
                        ["Finance","HR","IT","Operations","Sales","Accounting","Engineering","Quality","Marketing"] else 0)
            with col_b:
                new_location = st.selectbox("Location", ["Windsor HQ","Plant Floor"],
                    index=["Windsor HQ","Plant Floor"].index(asset["location"]) if asset["location"] in ["Windsor HQ","Plant Floor"] else 0)
                new_status   = st.selectbox("Status",
                    ["Active","Needs Refresh","Retired","Available"],
                    index=["Active","Needs Refresh","Retired","Available"].index(asset["status"])
                          if asset["status"] in ["Active","Needs Refresh","Retired","Available"] else 0)
                new_notes    = st.text_area("Notes", value=asset["notes"] or "")

            col_s, col_r, col_c = st.columns(3)
            with col_s:
                if st.button("💾 Save Changes", type="primary", use_container_width=True):
                    update_asset(asset["asset_id"], new_assigned, new_dept,
                                 new_location, new_status, new_notes, "IT Admin")
                    st.success(f"✅ {asset['asset_id']} updated successfully!")
                    st.session_state.edit_asset = None
                    st.rerun()
            with col_r:
                if st.button("🗑️ Retire Asset", use_container_width=True):
                    retire_asset(asset["asset_id"], "IT Admin")
                    st.warning(f"Asset {asset['asset_id']} has been retired.")
                    st.session_state.edit_asset = None
                    st.rerun()
            with col_c:
                if st.button("✖ Cancel", use_container_width=True):
                    st.session_state.edit_asset = None
                    st.rerun()

import streamlit as st
import pandas as pd
from database import get_audit_log

def render():
    st.markdown("""
    <div class="main-header">
        <h1>📁 Audit Trail</h1>
        <p>Complete change history for all IT assets — audit-ready documentation</p>
    </div>
    """, unsafe_allow_html=True)

    logs = get_audit_log()

    if not logs:
        st.info("No audit records yet. Changes to assets will appear here.")
        return

    df = pd.DataFrame([dict(l) for l in logs])

    st.markdown(f"**{len(df)} audit record(s)**")

    search = st.text_input("🔍 Search by Asset ID or changed by", "")
    if search:
        df = df[df["asset_id"].str.contains(search, case=False) |
                df["changed_by"].str.contains(search, case=False)]

    ACTION_ICONS = {"Updated": "✏️", "Retired": "🗑️", "Added": "➕"}

    for _, row in df.iterrows():
        icon = ACTION_ICONS.get(row["action"], "📝")
        st.markdown(f"""
        <div style="background:white; border:1px solid #e2e8f0; border-radius:8px;
             padding:0.8rem 1rem; margin-bottom:0.4rem;">
            {icon} <strong>{row['action']}</strong> — Asset <code>{row['asset_id']}</code>
            &nbsp;&nbsp;|&nbsp;&nbsp; 👤 {row['changed_by']}
            &nbsp;&nbsp;|&nbsp;&nbsp; 🕐 {row['changed_at']}<br>
            <small style="color:#718096">{row['details']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Audit Trail to CSV", csv,
                       "audit_trail.csv", "text/csv")

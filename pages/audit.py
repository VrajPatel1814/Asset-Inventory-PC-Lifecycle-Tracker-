import streamlit as st
import pandas as pd
from database import get_audit_log
from theme import THEME_CSS

ACTION_STYLE = {
    "Updated": ("✏️","#dbeafe","#1e3a8a"),
    "Retired":  ("📦","#fee2e2","#991b1b"),
    "Added":    ("➕","#d8f3dc","#1b4332"),
}

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🔍</div>
        <div class="page-header-text">
            <div class="eyebrow">Compliance</div>
            <h1>Audit Trail</h1>
            <p>Complete change history for every IT asset — audit-ready and exportable</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    logs = get_audit_log()
    if not logs:
        st.markdown('<div class="warn-pill">⚠️ &nbsp; No audit records yet — changes to assets will appear here automatically</div>',
                    unsafe_allow_html=True)
        return

    df = pd.DataFrame([dict(l) for l in logs])
    st.markdown(f'<p style="color:#6b7c6e;font-size:0.82rem;margin-bottom:0.75rem;">'
                f'<b style="color:#2d6a4f">{len(df)}</b> records · showing last 100 changes</p>',
                unsafe_allow_html=True)

    kw = st.text_input("Search", placeholder="Asset ID or changed by…")
    if kw:
        df = df[df["asset_id"].str.contains(kw, case=False) |
                df["changed_by"].str.contains(kw, case=False)]

    st.markdown('<div class="section-head">Change Log</div>', unsafe_allow_html=True)

    for _, row in df.iterrows():
        icon, bg, fg = ACTION_STYLE.get(row["action"], ("📝","#f4f6f3","#1a2e1d"))
        st.markdown(f"""
        <div class="asset-card" style="display:flex;align-items:flex-start;gap:12px;">
            <div style="background:{bg};border-radius:8px;padding:8px;font-size:1rem;
                        flex-shrink:0;margin-top:2px;">{icon}</div>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-weight:700;font-size:0.88rem;color:{fg};">
                            {row['action']}
                        </span>
                        &nbsp;
                        <span class="mono" style="color:#2d6a4f;font-size:0.8rem;
                              background:#d8f3dc;padding:2px 8px;border-radius:4px;">
                            {row['asset_id']}
                        </span>
                    </div>
                    <span style="font-size:0.75rem;color:#6b7c6e;">{row['changed_at']}</span>
                </div>
                <div style="margin-top:3px;font-size:0.8rem;color:#6b7c6e;">
                    By: <b>{row['changed_by']}</b> &nbsp;·&nbsp; {row['details']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_dl, _ = st.columns([1,3])
    with col_dl:
        csv = df.to_csv(index=False).encode()
        st.download_button("⬇ Export Audit Trail", csv, "audit_trail.csv", "text/csv",
                           use_container_width=True)

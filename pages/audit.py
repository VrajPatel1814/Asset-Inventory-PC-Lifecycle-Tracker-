import streamlit as st
import pandas as pd
from database import get_audit_log

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">COMPLIANCE</div>
        <div class="ops-title">Audit Trail</div>
        <p class="ops-sub">Immutable change history for all IT assets — exportable for audit review</p>
    </div>
    """, unsafe_allow_html=True)

    logs = get_audit_log()
    if not logs:
        st.markdown("""
        <div class="warn-bar">
            NO AUDIT RECORDS YET — Changes to assets will be logged here automatically.
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame([dict(l) for l in logs])
    st.markdown(f"""
    <div style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#64748b; margin-bottom:1rem;">
        {len(df)} RECORDS &nbsp;·&nbsp; SHOWING LAST 100 CHANGES &nbsp;·&nbsp;
        ALL TIMES ARE LOCAL
    </div>
    """, unsafe_allow_html=True)

    kw = st.text_input("SEARCH", placeholder="Asset ID or changed by...")
    if kw:
        df = df[df["asset_id"].str.contains(kw, case=False) |
                df["changed_by"].str.contains(kw, case=False)]

    ACTION_COLOR = {"Updated": "#f59e0b", "Retired": "#ef4444", "Added": "#22c55e"}

    st.markdown('<div class="section-label">CHANGE LOG</div>', unsafe_allow_html=True)

    for _, row in df.iterrows():
        color  = ACTION_COLOR.get(row["action"], "#94a3b8")
        symbol = {"Updated":"✎","Retired":"✕","Added":"+"}.get(row["action"],"·")
        st.markdown(f"""
        <div style="background:#141720; border:1px solid #2a2f3d; border-left:3px solid {color};
                    border-radius:4px; padding:0.65rem 1rem; margin-bottom:4px;
                    font-family:IBM Plex Mono,monospace; font-size:0.75rem;">
            <span style="color:{color}; font-weight:600;">{symbol} {row['action'].upper()}</span>
            &nbsp;·&nbsp;
            <span class="mono-tag">{row['asset_id']}</span>
            &nbsp;·&nbsp;
            <span style="color:#94a3b8;">{row['changed_by']}</span>
            &nbsp;·&nbsp;
            <span style="color:#64748b;">{row['changed_at']}</span><br>
            <span style="color:#64748b; font-size:0.7rem;">{row['details']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇ EXPORT AUDIT TRAIL", csv, "audit_trail.csv", "text/csv")

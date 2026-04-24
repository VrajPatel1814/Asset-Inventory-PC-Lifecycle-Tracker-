import streamlit as st
import pandas as pd
from database import get_onboarding_log

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">AUDIT RECORD</div>
        <div class="ops-title">Transition Log</div>
        <p class="ops-sub">Complete onboarding and offboarding history — exportable for compliance</p>
    </div>
    """, unsafe_allow_html=True)

    logs = get_onboarding_log()
    if not logs:
        st.markdown('<div class="warn-bar">NO TRANSITION RECORDS YET — Complete an onboarding or offboarding first.</div>',
                    unsafe_allow_html=True)
        return

    df = pd.DataFrame([dict(l) for l in logs])
    on_count  = len(df[df["log_type"] == "Onboarding"])
    off_count = len(df[df["log_type"] == "Offboarding"])

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="stat-tile m">
            <div class="stat-val">{len(df)}</div>
            <div class="stat-lbl">TOTAL TRANSITIONS</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-tile g">
            <div class="stat-val">{on_count}</div>
            <div class="stat-lbl">ONBOARDING EVENTS</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-tile t">
            <div class="stat-val">{off_count}</div>
            <div class="stat-lbl">OFFBOARDING EVENTS</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    ft = st.selectbox("FILTER BY TYPE", ["All","Onboarding","Offboarding"])
    filtered = df if ft == "All" else df[df["log_type"] == ft]

    st.markdown('<div class="section-label">RECORDS</div>', unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        is_on  = row["log_type"] == "Onboarding"
        color  = "#22c55e" if is_on else "#14b8a6"
        bg     = "rgba(34,197,94,0.06)" if is_on else "rgba(20,184,166,0.06)"
        symbol = "↓" if is_on else "↑"
        st.markdown(f"""
        <div style="background:{bg}; border:1px solid #2a2f3d; border-left:3px solid {color};
                    border-radius:4px; padding:0.8rem 1rem; margin-bottom:5px;">
            <span style="font-family:IBM Plex Mono,monospace; font-size:0.7rem;
                         color:{color}; font-weight:600; letter-spacing:0.1em;">
                {symbol} {row['log_type'].upper()}
            </span>
            &nbsp;·&nbsp;
            <span style="color:#e2e8f0; font-size:0.85rem; font-weight:600;">{row['employee_name']}</span>
            &nbsp;·&nbsp;
            <span style="color:#64748b; font-size:0.78rem;">{row['department']}</span>
            &nbsp;·&nbsp;
            <span style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#64748b;">
                {row['processed_at']}
            </span><br>
            <span style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#94a3b8;">
                ASSETS: {row['asset_ids']}
            </span>
            &nbsp;·&nbsp;
            <span style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#64748b;">
                BY: {row['processed_by']}
            </span>
            {"<br><span style='font-size:0.78rem;color:#64748b;'>" + row['notes'] + "</span>" if row['notes'] else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    csv = filtered.to_csv(index=False).encode()
    st.download_button("⬇ EXPORT LOG CSV", csv, "transition_log.csv", "text/csv")

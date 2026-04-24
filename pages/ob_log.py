import streamlit as st
import pandas as pd
from database import get_onboarding_log

def render():
    st.markdown("""
    <div class="main-header">
        <h1>📋 Onboarding & Offboarding Log</h1>
        <p>Full audit record of all employee equipment transitions</p>
    </div>
    """, unsafe_allow_html=True)

    logs = get_onboarding_log()

    if not logs:
        st.info("No onboarding or offboarding records yet.")
        return

    df = pd.DataFrame([dict(l) for l in logs])

    # Summary
    on_count  = len(df[df["log_type"] == "Onboarding"])
    off_count = len(df[df["log_type"] == "Offboarding"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="value">{len(df)}</div>
            <div class="label">Total Transitions</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="value">{on_count}</div>
            <div class="label">Onboarding Events</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="value">{off_count}</div>
            <div class="label">Offboarding Events</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter
    filter_type = st.selectbox("Filter by Type", ["All", "Onboarding", "Offboarding"])
    if filter_type != "All":
        df = df[df["log_type"] == filter_type]

    # Display
    for _, row in df.iterrows():
        icon = "👤" if row["log_type"] == "Onboarding" else "📤"
        color = "#f0fff4" if row["log_type"] == "Onboarding" else "#fff5f5"
        border = "#38a169" if row["log_type"] == "Onboarding" else "#e53e3e"
        st.markdown(f"""
        <div style="background:{color}; border-left:4px solid {border};
             border-radius:8px; padding:1rem; margin-bottom:0.5rem;">
            <strong>{icon} {row['log_type']} — {row['employee_name']}</strong>
            &nbsp;&nbsp;|&nbsp;&nbsp; {row['department']}
            &nbsp;&nbsp;|&nbsp;&nbsp; 🕐 {row['processed_at']}
            &nbsp;&nbsp;|&nbsp;&nbsp; 👤 Processed by: {row['processed_by']}<br>
            <small>Assets: <code>{row['asset_ids']}</code></small><br>
            {"<small>Notes: " + row['notes'] + "</small>" if row['notes'] else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Log to CSV", csv,
                       "onboarding_offboarding_log.csv", "text/csv")

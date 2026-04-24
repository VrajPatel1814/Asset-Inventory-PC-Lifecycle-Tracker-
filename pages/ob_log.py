import streamlit as st
import pandas as pd
from database import get_onboarding_log
from theme import THEME_CSS

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📋</div>
        <div class="page-header-text">
            <div class="eyebrow">Workforce</div>
            <h1>Transition Log</h1>
            <p>Complete onboarding and offboarding history — exportable for compliance</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    logs = get_onboarding_log()
    if not logs:
        st.markdown('<div class="warn-pill">⚠️ &nbsp; No records yet — complete an onboarding or offboarding first</div>',
                    unsafe_allow_html=True)
        return

    df = pd.DataFrame([dict(l) for l in logs])
    on_c  = len(df[df["log_type"] == "Onboarding"])
    off_c = len(df[df["log_type"] == "Offboarding"])

    c1, c2, c3 = st.columns(3)
    kpis = [
        (c1, str(len(df)),  "Total Transitions", "#f4f6f3","#1a2e1d","🔄"),
        (c2, str(on_c),     "Onboarding Events", "#d8f3dc","#1b4332","👋"),
        (c3, str(off_c),    "Offboarding Events","#fce7f3","#831843","🚪"),
    ]
    for col, val, lbl, bg, fg, icon in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:{bg};">{icon}</div>
                <div class="kpi-val" style="color:{fg};">{val}</div>
                <div class="kpi-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    ft = st.selectbox("Filter", ["All","Onboarding","Offboarding"])
    filt = df if ft == "All" else df[df["log_type"] == ft]

    st.markdown('<div class="section-head">Records</div>', unsafe_allow_html=True)

    for _, row in filt.iterrows():
        is_on  = row["log_type"] == "Onboarding"
        extra  = "" if is_on else "off"
        symbol = "👋" if is_on else "🚪"
        ltype  = row["log_type"]
        st.markdown(f"""
        <div class="transition-card {extra}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                                 letter-spacing:0.08em;color:{'#52b788' if is_on else '#e76f51'};">
                        {symbol} {ltype}
                    </span>
                    &nbsp;&nbsp;
                    <span style="font-weight:600;font-size:0.9rem;">{row['employee_name']}</span>
                    &nbsp;
                    <span style="color:#6b7c6e;font-size:0.82rem;">{row['department']}</span>
                </div>
                <span style="font-size:0.75rem;color:#6b7c6e;">{row['processed_at']}</span>
            </div>
            <div style="margin-top:5px;font-size:0.8rem;color:#6b7c6e;">
                Assets: <span class="mono">{row['asset_ids']}</span>
                &nbsp;·&nbsp; By: {row['processed_by']}
                {"&nbsp;·&nbsp; " + row['notes'] if row['notes'] else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_dl, _ = st.columns([1,3])
    with col_dl:
        csv = filt.to_csv(index=False).encode()
        st.download_button("⬇ Export Log", csv, "transition_log.csv", "text/csv",
                           use_container_width=True)

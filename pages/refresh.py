import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import get_refresh_candidates, get_all_assets
from theme import THEME_CSS

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🔄</div>
        <div class="page-header-text">
            <div class="eyebrow">Lifecycle Management</div>
            <h1>PC Refresh Planner</h1>
            <p>Devices exceeding the 3-year lifecycle threshold, prioritised for action</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    candidates = get_refresh_candidates(years=3)
    all_assets = get_all_assets()
    total      = len(all_assets)
    today      = pd.Timestamp(date.today())

    if not candidates:
        st.markdown('<div class="ok-pill">✅ &nbsp; All clear — every device is within its 3-year lifecycle</div>',
                    unsafe_allow_html=True)
        return

    df = pd.DataFrame([dict(c) for c in candidates])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    df["age_years"]     = ((today - df["purchase_date"]).dt.days / 365).round(2)

    critical = len(df[df["age_years"] >= 5])
    high     = len(df[(df["age_years"] >= 4) & (df["age_years"] < 5)])
    medium   = len(df[df["age_years"] < 4])

    # ── KPI CARDS ────────────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    kpis = [
        (c1, str(len(df)),  "Total Flagged",   f"{round(len(df)/total*100)}% of inventory",
         "#f4f6f3","#1a2e1d","📋"),
        (c2, str(critical), "Critical (5+ yrs)","Replace immediately",
         "#fee2e2","#991b1b","🔴"),
        (c3, str(high),     "High (4–5 yrs)",  "Schedule next quarter",
         "#ffedd5","#9a3412","🟠"),
        (c4, str(medium),   "Medium (3–4 yrs)","Budget next fiscal year",
         "#fef9c3","#713f12","🟡"),
    ]
    for col, val, lbl, sub, bg, fg, icon in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:{bg};">{icon}</div>
                <div class="kpi-val" style="color:{fg};">{val}</div>
                <div class="kpi-lbl">{lbl}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    PLOTLY = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans,sans-serif",color="#6b7c6e",size=10),
        margin=dict(t=10,b=30,l=10,r=10), height=260,
        xaxis=dict(gridcolor="#e2e8da",zeroline=False,linecolor="#e2e8da",
                   tickfont=dict(size=10,color="#6b7c6e")),
        yaxis=dict(gridcolor="#e2e8da",zeroline=False,linecolor="#e2e8da",
                   tickfont=dict(size=10,color="#6b7c6e")),
    )

    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="section-head">Refresh Need by Department</div>', unsafe_allow_html=True)
        d = df["department"].value_counts().reset_index()
        d.columns = ["Dept","Count"]
        fig1 = px.bar(d, x="Count", y="Dept", orientation="h", text="Count",
                      color="Count", color_continuous_scale=["#fef9c3","#c1121f"])
        fig1.update_layout(**PLOTLY, coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed",gridcolor="#e2e8da",
                                      zeroline=False,linecolor="#e2e8da",
                                      tickfont=dict(size=10,color="#6b7c6e")))
        fig1.update_traces(textposition="outside",textfont=dict(color="#6b7c6e",size=10),
                           marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)

    with cb:
        st.markdown('<div class="section-head">Refresh Need by Device Type</div>', unsafe_allow_html=True)
        t = df["device_type"].value_counts().reset_index()
        t.columns = ["Type","Count"]
        cmap = {"Laptop":"#e76f51","Desktop":"#e9c46a","Monitor":"#84a98c","Mobile Device":"#52b788"}
        fig2 = px.pie(t, names="Type", values="Count",
                      color="Type", color_discrete_map=cmap, hole=0.48)
        fig2.update_layout(**PLOTLY, legend=dict(orientation="h",y=-0.2,font=dict(size=10)))
        fig2.update_traces(textfont=dict(color="#6b7c6e",size=10))
        st.plotly_chart(fig2, use_container_width=True)

    # ── FULL TABLE ────────────────────────────────────────────────
    st.markdown('<div class="section-head" style="margin-top:0.5rem;">Full Candidate List — Oldest First</div>',
                unsafe_allow_html=True)

    export_df = df[["asset_id","device_type","brand","model","serial_number",
                    "assigned_to","department","location","purchase_date","age_years","status"]].copy()
    export_df.columns = ["Asset ID","Type","Brand","Model","Serial","Assigned To",
                         "Dept","Location","Purchase Date","Age (yrs)","Status"]
    export_df = export_df.sort_values("Age (yrs)", ascending=False)

    def row_style(row):
        if row["Age (yrs)"] >= 5:   return ["background-color:#fff5f5"]*len(row)
        elif row["Age (yrs)"] >= 4: return ["background-color:#fffbeb"]*len(row)
        else:                        return ["background-color:#fefce8"]*len(row)

    st.dataframe(export_df.style.apply(row_style, axis=1),
                 use_container_width=True, hide_index=True)

    col_dl, _ = st.columns([1,3])
    with col_dl:
        csv = export_df.to_csv(index=False).encode()
        st.download_button("⬇ Export Refresh Plan", csv, "refresh_plan.csv", "text/csv",
                           use_container_width=True)

    # ── ACTION PLAN ───────────────────────────────────────────────
    st.markdown('<div class="section-head" style="margin-top:1rem;">Recommended Action Plan</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#fff;border:1.5px solid #e2e8da;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(30,60,35,0.08);">
        <div class="action-plan-row">
            <span class="badge b-critical">Critical</span>
            <span style="font-weight:600;">{critical} devices — 5+ years old</span>
            <span style="color:#6b7c6e;font-size:0.82rem;">Replace immediately — end of supported lifecycle</span>
        </div>
        <div class="action-plan-row">
            <span class="badge b-high">High</span>
            <span style="font-weight:600;">{high} devices — 4–5 years old</span>
            <span style="color:#6b7c6e;font-size:0.82rem;">Schedule replacement within next quarter</span>
        </div>
        <div class="action-plan-row">
            <span class="badge b-medium">Medium</span>
            <span style="font-weight:600;">{medium} devices — 3–4 years old</span>
            <span style="color:#6b7c6e;font-size:0.82rem;">Monitor and plan budget for next fiscal year</span>
        </div>
        <div class="action-plan-row">
            <span class="badge b-active">OK</span>
            <span style="font-weight:600;">{total - len(df)} devices — within lifecycle</span>
            <span style="color:#6b7c6e;font-size:0.82rem;">No action required at this time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import get_refresh_candidates, get_all_assets

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">LIFECYCLE MANAGEMENT</div>
        <div class="ops-title">PC Refresh Planner</div>
        <p class="ops-sub">Devices exceeding 3-year lifecycle threshold — sorted by priority</p>
    </div>
    """, unsafe_allow_html=True)

    candidates = get_refresh_candidates(years=3)
    all_assets = get_all_assets()
    total      = len(all_assets)
    today      = pd.Timestamp(date.today())

    if not candidates:
        st.markdown('<div class="ok-bar">✓ ALL CLEAR — No devices currently require refresh.</div>',
                    unsafe_allow_html=True)
        return

    df = pd.DataFrame([dict(c) for c in candidates])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    df["age_years"]     = ((today - df["purchase_date"]).dt.days / 365).round(2)

    critical = len(df[df["age_years"] >= 5])
    high     = len(df[(df["age_years"] >= 4) & (df["age_years"] < 5)])
    medium   = len(df[df["age_years"] < 4])

    # ── STAT TILES ────────────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-tile">
            <div class="stat-val">{len(df)}</div>
            <div class="stat-lbl">TOTAL FLAGGED</div>
            <div style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:#64748b;margin-top:4px;">
            {round(len(df)/total*100)}% OF INVENTORY</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-tile r">
            <div class="stat-val">{critical}</div>
            <div class="stat-lbl">CRITICAL · 5+ YRS</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-tile">
            <div class="stat-val">{high}</div>
            <div class="stat-lbl">HIGH · 4–5 YRS</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-tile m">
            <div class="stat-val">{medium}</div>
            <div class="stat-lbl">MEDIUM · 3–4 YRS</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ───────────────────────────────────────────────────
    THEME = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                 font=dict(family="IBM Plex Mono,monospace",color="#94a3b8",size=9),
                 margin=dict(t=10,b=10,l=10,r=10), height=260)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-label">REFRESH NEED BY DEPARTMENT</div>',
                    unsafe_allow_html=True)
        dept_r = df["department"].value_counts().reset_index()
        dept_r.columns = ["Dept","Count"]
        fig1 = px.bar(dept_r, x="Count", y="Dept", orientation="h", text="Count",
                      color="Count", color_continuous_scale=["#1c2030","#ef4444"])
        fig1.update_layout(**THEME, coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed", gridcolor="#2a2f3d",
                                      zeroline=False, linecolor="#2a2f3d"),
                           xaxis=dict(gridcolor="#2a2f3d", zeroline=False))
        fig1.update_traces(textposition="outside", textfont_color="#94a3b8")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-label">REFRESH NEED BY DEVICE TYPE</div>',
                    unsafe_allow_html=True)
        type_r = df["device_type"].value_counts().reset_index()
        type_r.columns = ["Type","Count"]
        cmap   = {"Laptop":"#f59e0b","Desktop":"#ef4444","Monitor":"#64748b","Mobile Device":"#14b8a6"}
        fig2   = px.pie(type_r, names="Type", values="Count",
                        color="Type", color_discrete_map=cmap, hole=0.45)
        fig2.update_layout(**THEME, legend=dict(orientation="h", y=-0.2, font=dict(size=9)))
        fig2.update_traces(textfont_color="#94a3b8")
        st.plotly_chart(fig2, use_container_width=True)

    # ── FULL TABLE ────────────────────────────────────────────────
    st.markdown('<div class="section-label" style="margin-top:1rem;">FULL REFRESH CANDIDATE LIST — OLDEST FIRST</div>',
                unsafe_allow_html=True)

    export_df = df[["asset_id","device_type","brand","model","serial_number",
                    "assigned_to","department","location","purchase_date","age_years","status"]].copy()
    export_df.columns = ["Asset ID","Type","Brand","Model","Serial","Assigned To",
                         "Dept","Location","Purchase Date","Age (yrs)","Status"]
    export_df = export_df.sort_values("Age (yrs)", ascending=False)

    def row_color(row):
        if row["Age (yrs)"] >= 5:   return ["background-color:#1a1020"] * len(row)
        elif row["Age (yrs)"] >= 4: return ["background-color:#141410"] * len(row)
        else:                        return ["background-color:#141720"] * len(row)

    st.dataframe(export_df.style.apply(row_color, axis=1),
                 use_container_width=True, hide_index=True)

    csv = export_df.to_csv(index=False).encode()
    st.download_button("⬇ EXPORT REFRESH PLAN", csv, "pc_refresh_plan.csv", "text/csv")

    # ── ACTION PLAN ───────────────────────────────────────────────
    st.markdown('<div class="section-label" style="margin-top:1.2rem;">RECOMMENDED ACTION PLAN</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#141720; border:1px solid #2a2f3d; border-radius:6px; padding:1rem;
                font-family:IBM Plex Mono,monospace; font-size:0.78rem; line-height:2.2;">
        <span class="prio-c">■ CRITICAL ({critical} devices, 5+ yrs)</span>
        &nbsp;→&nbsp; Replace immediately — end of supported lifecycle<br>
        <span class="prio-h">■ HIGH ({high} devices, 4–5 yrs)</span>
        &nbsp;→&nbsp; Schedule replacement within next quarter<br>
        <span class="prio-m">■ MEDIUM ({medium} devices, 3–4 yrs)</span>
        &nbsp;→&nbsp; Monitor — plan budget for next fiscal year<br>
        <span style="color:#22c55e;">■ ALL OTHERS ({total - len(df)} devices)</span>
        &nbsp;→&nbsp; No action required
    </div>
    """, unsafe_allow_html=True)

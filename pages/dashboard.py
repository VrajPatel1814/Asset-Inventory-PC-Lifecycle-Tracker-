import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from database import get_all_assets, get_refresh_candidates
from theme import THEME_CSS

PLOTLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#6b7c6e", size=11),
    margin=dict(t=10, b=30, l=10, r=10),
    height=270,
    xaxis=dict(gridcolor="#e2e8da", zeroline=False, linecolor="#e2e8da",
               tickfont=dict(size=10, color="#6b7c6e")),
    yaxis=dict(gridcolor="#e2e8da", zeroline=False, linecolor="#e2e8da",
               tickfont=dict(size=10, color="#6b7c6e")),
)

def render():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📊</div>
        <div class="page-header-text">
            <div class="eyebrow">Overview</div>
            <h1>Asset Dashboard</h1>
            <p>Live inventory health across all Plasman facilities</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    assets  = get_all_assets()
    df      = pd.DataFrame([dict(a) for a in assets])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    today   = pd.Timestamp(date.today())
    df["age_years"] = ((today - df["purchase_date"]).dt.days / 365).round(1)

    refresh   = get_refresh_candidates(years=3)
    ref_count = len(refresh)
    total     = len(df)
    active    = len(df[df["status"] == "Active"])
    need_ref  = len(df[df["status"] == "Needs Refresh"])
    retired   = len(df[df["status"] == "Retired"])
    hq        = len(df[df["location"] == "Windsor HQ"])
    plant     = len(df[df["location"] == "Plant Floor"])

    # ── KPI CARDS ────────────────────────────────────────────────
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1, str(total),    "Total Assets",    "#d8f3dc", "#2d6a4f", "🗂️"),
        (c2, str(active),   "Active",          "#d8f3dc", "#1b4332", "✅"),
        (c3, str(need_ref), "Needs Refresh",   "#fef3c7", "#78350f", "⚠️"),
        (c4, str(retired),  "Retired",         "#f1f5f9", "#475569", "📦"),
        (c5, str(hq),       "Windsor HQ",      "#dbeafe", "#1e3a8a", "🏢"),
        (c6, str(plant),    "Plant Floor",     "#ede9fe", "#4c1d95", "🏭"),
    ]
    for col, val, lbl, bg, fg, icon in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:{bg};">{icon}</div>
                <div class="kpi-val" style="color:{fg};">{val}</div>
                <div class="kpi-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ALERT ──────────────────────────────────────────────────
    if ref_count > 0:
        critical_n = len([r for r in refresh if
            (today - pd.Timestamp(r["purchase_date"])).days / 365 >= 5])
        st.markdown(f"""
        <div class="alert-pill">
            ⚠️ &nbsp;
            <b>{ref_count} devices need refresh</b> &nbsp;·&nbsp;
            {critical_n} critical (5+ yrs) &nbsp;·&nbsp;
            See Refresh Planner
        </div>
        """, unsafe_allow_html=True)

    # ── CHARTS ROW 1 ─────────────────────────────────────────────
    ca, cb, cc = st.columns(3)

    with ca:
        st.markdown('<div class="section-head">Status Breakdown</div>', unsafe_allow_html=True)
        with st.container():
            s_df  = df["status"].value_counts().reset_index()
            s_df.columns = ["Status","Count"]
            cmap  = {"Active":"#52b788","Needs Refresh":"#e9c46a",
                     "Retired":"#94a3b8","Available":"#60a5fa"}
            fig1  = px.pie(s_df, names="Status", values="Count",
                           color="Status", color_discrete_map=cmap, hole=0.52)
            fig1.update_layout(**PLOTLY)
            fig1.update_layout(legend=dict(orientation="h",y=-0.18,font=dict(size=10)))
            fig1.update_traces(textfont=dict(color="#6b7c6e", size=10))
            st.plotly_chart(fig1, use_container_width=True)

    with cb:
        st.markdown('<div class="section-head">Device Types</div>', unsafe_allow_html=True)
        t_df = df["device_type"].value_counts().reset_index()
        t_df.columns = ["Type","Count"]
        fig2 = px.bar(t_df, x="Type", y="Count", text="Count",
                      color="Type",
                      color_discrete_sequence=["#2d6a4f","#52b788","#84a98c","#b7e4c7"])
        fig2.update_layout(**PLOTLY, showlegend=False)
        fig2.update_traces(textposition="outside",
                           textfont=dict(color="#6b7c6e", size=10), marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    with cc:
        st.markdown('<div class="section-head">Location vs Status</div>', unsafe_allow_html=True)
        loc_df = df.groupby(["location","status"]).size().reset_index(name="Count")
        cmap2  = {"Active":"#52b788","Needs Refresh":"#e9c46a",
                  "Retired":"#94a3b8","Available":"#60a5fa"}
        fig3   = px.bar(loc_df, x="location", y="Count", color="status",
                        barmode="stack", color_discrete_map=cmap2)
        fig3.update_layout(**PLOTLY, xaxis_title="", legend_title="")
        fig3.update_layout(legend=dict(orientation="h", y=-0.18, font=dict(size=10)))
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    # ── CHARTS ROW 2 ─────────────────────────────────────────────
    cd, ce = st.columns([1.5, 1])

    with cd:
        st.markdown('<div class="section-head">Assets by Department</div>', unsafe_allow_html=True)
        d_df = df["department"].value_counts().reset_index()
        d_df.columns = ["Dept","Count"]
        fig4 = px.bar(d_df, x="Count", y="Dept", orientation="h", text="Count",
                      color="Count", color_continuous_scale=["#b7e4c7","#2d6a4f"])
        fig4.update_layout(**PLOTLY, height=300, coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed", gridcolor="#e2e8da",
                                      zeroline=False, linecolor="#e2e8da",
                                      tickfont=dict(size=10,color="#6b7c6e")))
        fig4.update_traces(textposition="outside",
                           textfont=dict(color="#6b7c6e",size=10), marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

    with ce:
        st.markdown('<div class="section-head">Device Age Distribution</div>', unsafe_allow_html=True)
        age_df = df[df["status"] != "Retired"]
        fig5   = go.Figure()
        fig5.add_trace(go.Histogram(
            x=age_df["age_years"], nbinsx=16,
            marker_color="#52b788", opacity=0.8,
            marker_line_color="#2d6a4f", marker_line_width=0.5
        ))
        fig5.add_vline(x=3, line_dash="dot", line_color="#e76f51", line_width=2,
                       annotation_text="3yr threshold",
                       annotation_font_color="#e76f51", annotation_font_size=10,
                       annotation_position="top right")
        fig5.update_layout(**PLOTLY, height=300, showlegend=False,
                           xaxis_title="Age (years)", yaxis_title="Devices")
        st.plotly_chart(fig5, use_container_width=True)

    # ── OLDEST DEVICES TABLE ─────────────────────────────────────
    if ref_count > 0:
        st.markdown('<div class="section-head" style="margin-top:0.5rem;">Oldest Devices — Immediate Attention Required</div>',
                    unsafe_allow_html=True)
        ref_df = pd.DataFrame([dict(r) for r in refresh[:10]])
        ref_df["Age (yrs)"] = ((today - pd.to_datetime(ref_df["purchase_date"])).dt.days / 365).round(1)
        ref_df["purchase_date"] = pd.to_datetime(ref_df["purchase_date"]).dt.date
        cols = ["asset_id","device_type","brand","model","assigned_to","department","location","purchase_date","Age (yrs)","status"]
        st.dataframe(ref_df[cols], use_container_width=True, hide_index=True)

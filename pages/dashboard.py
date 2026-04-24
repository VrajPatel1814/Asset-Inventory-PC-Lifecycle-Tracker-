import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from database import get_all_assets, get_refresh_candidates

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono, monospace", color="#94a3b8", size=10),
    margin=dict(t=10, b=10, l=10, r=10),
    height=280,
    xaxis=dict(gridcolor="#2a2f3d", zeroline=False, linecolor="#2a2f3d"),
    yaxis=dict(gridcolor="#2a2f3d", zeroline=False, linecolor="#2a2f3d"),
)

def render():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-tag">SYSTEM OVERVIEW</div>
        <div class="ops-title">Asset Control Dashboard</div>
        <p class="ops-sub">Real-time inventory health across Plasman facilities</p>
    </div>
    """, unsafe_allow_html=True)

    assets  = get_all_assets()
    df      = pd.DataFrame([dict(a) for a in assets])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    today   = pd.Timestamp(date.today())
    df["age_years"] = ((today - df["purchase_date"]).dt.days / 365).round(1)

    refresh    = get_refresh_candidates(years=3)
    ref_count  = len(refresh)
    total      = len(df)
    active     = len(df[df["status"] == "Active"])
    needs_ref  = len(df[df["status"] == "Needs Refresh"])
    retired    = len(df[df["status"] == "Retired"])
    hq         = len(df[df["location"] == "Windsor HQ"])
    plant      = len(df[df["location"] == "Plant Floor"])

    # ── STAT TILES ────────────────────────────────────────────────
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    tiles = [
        (c1, str(total),    "TOTAL ASSETS",    ""),
        (c2, str(active),   "ACTIVE",          "g"),
        (c3, str(needs_ref),"NEEDS REFRESH",   ""),
        (c4, str(retired),  "RETIRED",         "m"),
        (c5, str(hq),       "WINDSOR HQ",      "t"),
        (c6, str(plant),    "PLANT FLOOR",     "t"),
    ]
    for col, val, lbl, cls in tiles:
        with col:
            st.markdown(f"""
            <div class="stat-tile {cls}">
                <div class="stat-val">{val}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ALERT BANNER ──────────────────────────────────────────────
    if ref_count > 0:
        critical_r = len([r for r in refresh if
            (today - pd.Timestamp(r["purchase_date"])).days / 365 >= 5])
        st.markdown(f"""
        <div class="alert-bar">
            ⚠  {ref_count} DEVICES FLAGGED FOR REFRESH
            ({round(ref_count/total*100)}% of inventory) ·
            {critical_r} CRITICAL (5+ years) ·
            See REFRESH PLANNER for full report
        </div>
        """, unsafe_allow_html=True)

    # ── ROW 1 ─────────────────────────────────────────────────────
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="section-label">STATUS DISTRIBUTION</div>', unsafe_allow_html=True)
        with st.container():
            status_df = df["status"].value_counts().reset_index()
            status_df.columns = ["Status","Count"]
            cmap = {"Active":"#22c55e","Needs Refresh":"#f59e0b","Retired":"#64748b","Available":"#14b8a6"}
            fig  = px.pie(status_df, names="Status", values="Count",
                          color="Status", color_discrete_map=cmap, hole=0.5)
            fig.update_layout(**PLOTLY_THEME)
            fig.update_layout(legend=dict(orientation="h", y=-0.15, font=dict(size=9)))
            fig.update_traces(textfont_color="#94a3b8")
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-label">DEVICE TYPES</div>', unsafe_allow_html=True)
        type_df = df["device_type"].value_counts().reset_index()
        type_df.columns = ["Type","Count"]
        fig2 = px.bar(type_df, x="Type", y="Count", text="Count",
                      color="Count", color_continuous_scale=["#1c2030","#f59e0b"])
        fig2.update_layout(**PLOTLY_THEME, showlegend=False, coloraxis_showscale=False)
        fig2.update_traces(textposition="outside", textfont_color="#94a3b8")
        st.plotly_chart(fig2, use_container_width=True)

    with col_c:
        st.markdown('<div class="section-label">ASSETS BY LOCATION</div>', unsafe_allow_html=True)
        loc_df = df.groupby(["location","status"]).size().reset_index(name="Count")
        cmap2  = {"Active":"#22c55e","Needs Refresh":"#f59e0b","Retired":"#64748b","Available":"#14b8a6"}
        fig3   = px.bar(loc_df, x="location", y="Count", color="status",
                        barmode="stack", color_discrete_map=cmap2, text_auto=True)
        fig3.update_layout(**PLOTLY_THEME, xaxis_title="", legend_title="")
        fig3.update_layout(legend=dict(orientation="h", y=-0.2, font=dict(size=9)))
        st.plotly_chart(fig3, use_container_width=True)

    # ── ROW 2 ─────────────────────────────────────────────────────
    col_d, col_e = st.columns([1.4, 1])

    with col_d:
        st.markdown('<div class="section-label">ASSETS BY DEPARTMENT</div>', unsafe_allow_html=True)
        dept_df = df["department"].value_counts().reset_index()
        dept_df.columns = ["Dept","Count"]
        fig4 = px.bar(dept_df, x="Count", y="Dept", orientation="h", text="Count",
                      color="Count", color_continuous_scale=["#1c2030","#14b8a6"])
        fig4.update_layout(**PLOTLY_THEME, height=300, coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed", gridcolor="#2a2f3d",
                                      zeroline=False, linecolor="#2a2f3d"))
        fig4.update_traces(textposition="outside", textfont_color="#94a3b8")
        st.plotly_chart(fig4, use_container_width=True)

    with col_e:
        st.markdown('<div class="section-label">AGE PROFILE</div>', unsafe_allow_html=True)
        age_df = df[df["status"] != "Retired"]
        fig5 = go.Figure()
        fig5.add_trace(go.Histogram(
            x=age_df["age_years"], nbinsx=18,
            marker_color="#f59e0b", opacity=0.7,
            name="Devices"
        ))
        fig5.add_vline(x=3, line_dash="dash", line_color="#ef4444", line_width=1.5,
                       annotation_text="3yr", annotation_font_color="#ef4444",
                       annotation_font_size=9)
        fig5.update_layout(**PLOTLY_THEME, height=300,
                           xaxis_title="Age (years)", yaxis_title="Count",
                           showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    # ── REFRESH PREVIEW TABLE ─────────────────────────────────────
    if ref_count > 0:
        st.markdown('<div class="section-label" style="margin-top:1rem;">TOP 8 — OLDEST DEVICES</div>',
                    unsafe_allow_html=True)
        ref_df = pd.DataFrame([dict(r) for r in refresh[:8]])
        ref_df["purchase_date"] = pd.to_datetime(ref_df["purchase_date"]).dt.date
        ref_df["Age (yrs)"]     = ((today - pd.to_datetime(ref_df["purchase_date"])).dt.days / 365).round(1)
        display_cols = ["asset_id","device_type","brand","model","assigned_to","department","purchase_date","Age (yrs)","status"]
        st.dataframe(ref_df[display_cols], use_container_width=True, hide_index=True)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import get_all_assets, get_refresh_candidates

def render():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Asset Management Dashboard</h1>
        <p>Real-time overview of all IT assets across Plasman facilities</p>
    </div>
    """, unsafe_allow_html=True)

    assets   = get_all_assets()
    df       = pd.DataFrame([dict(a) for a in assets])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    today    = pd.Timestamp(date.today())
    df["age_years"] = ((today - df["purchase_date"]).dt.days / 365).round(1)

    refresh_candidates = get_refresh_candidates(years=3)
    refresh_count      = len(refresh_candidates)

    # ── KPI CARDS ────────────────────────────────────────────────
    total     = len(df)
    active    = len(df[df["status"] == "Active"])
    needs_ref = len(df[df["status"] == "Needs Refresh"])
    retired   = len(df[df["status"] == "Retired"])
    hq_count  = len(df[df["location"] == "Windsor HQ"])
    plant_count = len(df[df["location"] == "Plant Floor"])

    cols = st.columns(6)
    metrics = [
        (str(total),       "Total Assets"),
        (str(active),      "Active"),
        (str(needs_ref),   "Needs Refresh"),
        (str(retired),     "Retired"),
        (str(hq_count),    "Windsor HQ"),
        (str(plant_count), "Plant Floor"),
    ]
    for col, (val, label) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="value">{val}</div>
                <div class="label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── REFRESH ALERT BANNER ─────────────────────────────────────
    if refresh_count > 0:
        st.markdown(f"""
        <div class="alert-card">
            ⚠️ <strong>{refresh_count} devices ({round(refresh_count/total*100)}% of inventory)
            are flagged for PC refresh</strong> — purchased more than 3 years ago.
            Visit the <strong>PC Refresh Planner</strong> for details.
        </div>
        """, unsafe_allow_html=True)

    # ── PANEL 1: Status + Device Type ────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🟢 Asset Status Breakdown")
        status_df = df["status"].value_counts().reset_index()
        status_df.columns = ["Status", "Count"]
        color_map = {"Active": "#38a169", "Needs Refresh": "#d69e2e",
                     "Retired": "#718096", "Available": "#3182ce"}
        fig1 = px.pie(status_df, names="Status", values="Count",
                      color="Status", color_discrete_map=color_map, hole=0.45)
        fig1.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300,
                           legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### 🖥️ Device Type Distribution")
        type_df = df["device_type"].value_counts().reset_index()
        type_df.columns = ["Device Type", "Count"]
        fig2 = px.bar(type_df, x="Device Type", y="Count",
                      color="Device Type", text="Count")
        fig2.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300,
                           showlegend=False)
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── PANEL 2: Department + Location ───────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 🏢 Assets by Department")
        dept_df = df["department"].value_counts().reset_index()
        dept_df.columns = ["Department", "Count"]
        fig3 = px.bar(dept_df, x="Count", y="Department", orientation="h",
                      color="Count", color_continuous_scale="Blues", text="Count")
        fig3.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=320,
                           coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 📍 Assets by Location & Status")
        loc_status = df.groupby(["location", "status"]).size().reset_index(name="Count")
        fig4 = px.bar(loc_status, x="location", y="Count", color="status",
                      barmode="stack",
                      color_discrete_map={"Active":"#38a169","Needs Refresh":"#d69e2e",
                                          "Retired":"#718096","Available":"#3182ce"},
                      text_auto=True)
        fig4.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=320,
                           xaxis_title="Location", legend_title="Status")
        st.plotly_chart(fig4, use_container_width=True)

    # ── PANEL 3: Age distribution ─────────────────────────────────
    st.markdown("#### 📅 Asset Age Distribution (Active & Needs Refresh)")
    age_df = df[df["status"] != "Retired"].copy()
    fig5   = px.histogram(age_df, x="age_years", nbins=20,
                          color="device_type",
                          labels={"age_years": "Age (Years)", "count": "Number of Devices"},
                          title="")
    fig5.add_vline(x=3, line_dash="dash", line_color="red",
                   annotation_text="3-yr refresh threshold",
                   annotation_position="top right")
    fig5.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300,
                       bargap=0.1, legend_title="Device Type")
    st.plotly_chart(fig5, use_container_width=True)

    # ── REFRESH TABLE PREVIEW ─────────────────────────────────────
    st.markdown("---")
    st.markdown("#### ⚠️ Top 10 Devices Due for Refresh")
    ref_df = pd.DataFrame([dict(r) for r in refresh_candidates[:10]])
    if not ref_df.empty:
        ref_df["purchase_date"] = pd.to_datetime(ref_df["purchase_date"]).dt.date
        ref_df["Age (yrs)"] = ((today - pd.to_datetime(ref_df["purchase_date"])).dt.days / 365).round(1)
        st.dataframe(
            ref_df[["asset_id","device_type","brand","model","assigned_to","department","purchase_date","Age (yrs)","status"]],
            use_container_width=True, hide_index=True
        )

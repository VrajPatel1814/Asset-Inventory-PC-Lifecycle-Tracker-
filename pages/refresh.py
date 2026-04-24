import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import get_refresh_candidates, get_all_assets

def render():
    st.markdown("""
    <div class="main-header">
        <h1>🔄 PC Refresh Planner</h1>
        <p>Proactive lifecycle management — identify and prioritize devices due for replacement</p>
    </div>
    """, unsafe_allow_html=True)

    candidates = get_refresh_candidates(years=3)
    all_assets = get_all_assets()
    total      = len(all_assets)
    today      = pd.Timestamp(date.today())

    if not candidates:
        st.success("✅ No devices currently require refresh. All assets are within their 3-year lifecycle.")
        return

    df = pd.DataFrame([dict(c) for c in candidates])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    df["age_years"]     = ((today - df["purchase_date"]).dt.days / 365).round(2)
    df["age_years_int"] = df["age_years"].astype(int)

    # Priority score: older = higher score
    df["refresh_priority"] = pd.cut(
        df["age_years"],
        bins=[0, 4, 5, 6, 100],
        labels=["Medium (3–4 yrs)", "High (4–5 yrs)", "Critical (5–6 yrs)", "Critical (6+ yrs)"]
    )

    # ── SUMMARY ──────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    critical = len(df[df["age_years"] >= 5])
    high     = len(df[(df["age_years"] >= 4) & (df["age_years"] < 5)])
    medium   = len(df[df["age_years"] < 4])

    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="value">{len(df)}</div>
            <div class="label">Total Flagged ({round(len(df)/total*100)}% of inventory)</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card" style="border-left-color:#e53e3e">
            <div class="value" style="color:#e53e3e">{critical}</div>
            <div class="label">Critical (5+ years old)</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card" style="border-left-color:#dd6b20">
            <div class="value" style="color:#dd6b20">{high}</div>
            <div class="label">High Priority (4–5 years)</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card" style="border-left-color:#d69e2e">
            <div class="value" style="color:#d69e2e">{medium}</div>
            <div class="label">Medium Priority (3–4 years)</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ───────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🏢 Refresh Need by Department")
        dept_refresh = df["department"].value_counts().reset_index()
        dept_refresh.columns = ["Department", "Devices to Refresh"]
        fig1 = px.bar(dept_refresh, x="Devices to Refresh", y="Department",
                      orientation="h", color="Devices to Refresh",
                      color_continuous_scale="Reds", text="Devices to Refresh")
        fig1.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300,
                           coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown("#### 🖥️ Refresh Need by Device Type")
        type_refresh = df["device_type"].value_counts().reset_index()
        type_refresh.columns = ["Device Type", "Count"]
        fig2 = px.pie(type_refresh, names="Device Type", values="Count", hole=0.4)
        fig2.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=300,
                           legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig2, use_container_width=True)

    # ── FULL REFRESH LIST ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 Full Refresh Candidate List — Sorted by Age (Oldest First)")

    export_df = df[["asset_id","device_type","brand","model","serial_number",
                    "assigned_to","department","location","purchase_date",
                    "age_years","refresh_priority","status"]].copy()
    export_df.columns = ["Asset ID","Type","Brand","Model","Serial #","Assigned To",
                         "Department","Location","Purchase Date","Age (yrs)","Priority","Status"]
    export_df = export_df.sort_values("Age (yrs)", ascending=False)

    # Color rows by priority
    def color_priority(row):
        if row["Age (yrs)"] >= 5:   return ["background-color: #fff5f5"] * len(row)
        elif row["Age (yrs)"] >= 4: return ["background-color: #fffaf0"] * len(row)
        else:                        return ["background-color: #fffff0"] * len(row)

    st.dataframe(
        export_df.style.apply(color_priority, axis=1),
        use_container_width=True, hide_index=True
    )

    csv = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Refresh Plan to CSV", csv,
                       "pc_refresh_plan.csv", "text/csv")

    # ── RECOMMENDATION BOX ────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 💡 Recommended Action Plan")
    st.markdown(f"""
    | Priority | Count | Recommended Action |
    |---|---|---|
    | 🔴 Critical (5+ yrs) | {critical} devices | **Replace immediately** — end of supported lifecycle |
    | 🟠 High (4–5 yrs) | {high} devices | **Schedule replacement** within next quarter |
    | 🟡 Medium (3–4 yrs) | {medium} devices | **Monitor** — plan budget for next fiscal year |
    | ✅ All others | {total - len(df)} devices | No action required |
    """)

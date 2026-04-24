import streamlit as st
from database import init_db

st.set_page_config(
    page_title="Plasman IT Asset Tracker",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# ── GLOBAL CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1a1a2e; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;
        text-align: center; color: white;
    }
    .main-header h1 { color: white; font-size: 2.2rem; margin: 0; }
    .main-header p  { color: #a0aec0; margin: 0.5rem 0 0 0; }
    .metric-card {
        background: white; border-radius: 10px; padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #0f3460; text-align: center;
    }
    .metric-card .value { font-size: 2rem; font-weight: 700; color: #0f3460; }
    .metric-card .label { font-size: 0.85rem; color: #718096; margin-top: 0.2rem; }
    .alert-card {
        background: #fff5f5; border-left: 4px solid #e53e3e;
        border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;
    }
    .warn-card {
        background: #fffaf0; border-left: 4px solid #dd6b20;
        border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;
    }
    .ok-card {
        background: #f0fff4; border-left: 4px solid #38a169;
        border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;
    }
    div[data-testid="stButton"] button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🖥️ IT Asset Tracker")
    st.markdown("**Plasman Global HQ**")
    st.markdown("---")

    pages = {
        "📊 Dashboard":            "dashboard",
        "🖥️ Asset Inventory":      "inventory",
        "🔄 PC Refresh Planner":   "refresh",
        "👤 Onboarding":           "onboarding",
        "📤 Offboarding":          "offboarding",
        "📋 Onboarding Log":       "log",
        "➕ Add New Asset":        "add_asset",
        "📁 Audit Trail":          "audit",
    }

    for label, key in pages.items():
        active = st.session_state.current_page == key
        if st.button(label, use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.current_page = key
            st.rerun()

    st.markdown("---")
    st.caption(f"75 assets tracked  \n2 locations  \n8 departments")

# ── PAGE ROUTER ───────────────────────────────────────────────────
page = st.session_state.current_page

if   page == "dashboard":  from pages.dashboard  import render
elif page == "inventory":  from pages.inventory  import render
elif page == "refresh":    from pages.refresh    import render
elif page == "onboarding": from pages.onboarding import render
elif page == "offboarding":from pages.offboarding import render
elif page == "log":        from pages.ob_log     import render
elif page == "add_asset":  from pages.add_asset  import render
elif page == "audit":      from pages.audit      import render
else:                      from pages.dashboard  import render

render()

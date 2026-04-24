import streamlit as st
from database import init_db
from theme import THEME_CSS

st.set_page_config(
    page_title="AssetIQ — Plasman IT",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.25rem 0 1.5rem 0; border-bottom: 1px solid rgba(216,243,220,0.2);
                margin-bottom: 1.25rem;">
        <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff;
                    letter-spacing: -0.03em; margin-bottom: 2px;">
            🌿 AssetIQ
        </div>
        <div style="font-size: 0.72rem; color: rgba(216,243,220,0.6);
                    font-weight: 500; letter-spacing: 0.04em;">
            Plasman IT · Asset Management
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_groups = {
        "OVERVIEW": [
            ("📊  Dashboard",       "dashboard"),
            ("🗂️  Asset Inventory", "inventory"),
        ],
        "LIFECYCLE": [
            ("🔄  Refresh Planner", "refresh"),
            ("➕  Add New Asset",   "add_asset"),
        ],
        "WORKFORCE": [
            ("👋  Onboarding",      "onboarding"),
            ("🚪  Offboarding",     "offboarding"),
            ("📋  Transition Log",  "log"),
        ],
        "COMPLIANCE": [
            ("🔍  Audit Trail",     "audit"),
        ],
    }

    for group_label, items in nav_groups.items():
        st.markdown(f"""
        <div style="font-size:0.62rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.12em; color:rgba(216,243,220,0.4);
                    margin: 0.9rem 0 0.35rem 0; padding-left:2px;">
            {group_label}
        </div>
        """, unsafe_allow_html=True)
        for label, key in items:
            active = st.session_state.current_page == key
            if st.button(label, use_container_width=True,
                         type="primary" if active else "secondary",
                         key=f"nav_{key}"):
                st.session_state.current_page = key
                st.rerun()

    st.markdown("""
    <div style="position:absolute; bottom:1.5rem; left:1rem; right:1rem;">
        <div style="background:rgba(216,243,220,0.1); border:1px solid rgba(216,243,220,0.15);
                    border-radius:8px; padding:0.75rem 0.9rem;">
            <div style="font-size:0.7rem; color:rgba(216,243,220,0.5); font-weight:600;
                        text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
                System Status
            </div>
            <div style="font-size:0.78rem; color:rgba(216,243,220,0.8); line-height:1.9;">
                75 assets tracked<br>
                2 site locations<br>
                8 departments
            </div>
            <div style="margin-top:8px; display:flex; align-items:center; gap:6px;">
                <div style="width:7px; height:7px; background:#52b788;
                            border-radius:50%; box-shadow:0 0 6px #52b788;"></div>
                <span style="font-size:0.7rem; color:rgba(216,243,220,0.6);">Database connected</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── PAGE ROUTER ───────────────────────────────────────────────────
page = st.session_state.current_page
if   page == "dashboard":   from pages.dashboard   import render
elif page == "inventory":   from pages.inventory   import render
elif page == "refresh":     from pages.refresh     import render
elif page == "onboarding":  from pages.onboarding  import render
elif page == "offboarding": from pages.offboarding import render
elif page == "log":         from pages.ob_log      import render
elif page == "add_asset":   from pages.add_asset   import render
elif page == "audit":       from pages.audit       import render
else:                       from pages.dashboard   import render
render()

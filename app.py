import streamlit as st
from database import init_db

st.set_page_config(
    page_title="IT Asset Control — Plasman",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# ── INDUSTRIAL / OPS THEME ────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

    :root {
        --bg:         #0d0f12;
        --surface:    #141720;
        --surface2:   #1c2030;
        --border:     #2a2f3d;
        --amber:      #f59e0b;
        --amber-dim:  #92610a;
        --amber-glow: rgba(245,158,11,0.12);
        --teal:       #14b8a6;
        --red:        #ef4444;
        --green:      #22c55e;
        --text:       #e2e8f0;
        --muted:      #64748b;
        --dim:        #94a3b8;
        --mono:       'IBM Plex Mono', monospace;
    }

    .stApp, [data-testid="stAppViewContainer"] { background: var(--bg) !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    .block-container { padding-top: 1.2rem !important; max-width: 100% !important; }

    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }
    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--dim) !important;
        font-family: var(--mono) !important;
        font-size: 0.75rem !important;
        text-align: left !important;
        letter-spacing: 0.04em;
        transition: all 0.15s;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        border-color: var(--amber) !important;
        color: var(--amber) !important;
        background: var(--amber-glow) !important;
    }
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        border-color: var(--amber) !important;
        color: var(--amber) !important;
        background: var(--amber-glow) !important;
    }

    p, li, span, label { color: var(--text); }
    h1,h2,h3,h4 { color: var(--text) !important; font-family: 'IBM Plex Sans', sans-serif; }

    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        background: var(--surface2) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 4px !important;
    }
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: var(--amber) !important;
        box-shadow: 0 0 0 2px var(--amber-glow) !important;
    }

    .stButton button {
        background: var(--surface2) !important;
        border: 1px solid var(--border) !important;
        color: var(--dim) !important;
        border-radius: 4px !important;
        font-family: var(--mono) !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        transition: all 0.15s !important;
    }
    .stButton button:hover { border-color: var(--amber) !important; color: var(--amber) !important; }
    .stButton button[kind="primary"] {
        background: var(--amber) !important;
        border-color: var(--amber) !important;
        color: #000 !important;
    }

    [data-testid="stDataFrame"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
    }
    [data-testid="stExpander"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
    }
    [data-testid="stForm"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 1.2rem !important;
    }
    .stDownloadButton button {
        background: transparent !important;
        border: 1px solid var(--teal) !important;
        color: var(--teal) !important;
        font-family: var(--mono) !important;
        font-size: 0.75rem !important;
    }
    .stMultiSelect span { background: var(--surface2) !important; color: var(--amber) !important; }
    hr { border-color: var(--border) !important; }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

    /* ── CUSTOM COMPONENTS ── */
    .ops-header { border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 1.5rem; }
    .ops-tag {
        font-family: var(--mono); font-size: 0.65rem; color: var(--amber);
        letter-spacing: 0.15em; text-transform: uppercase;
        background: var(--amber-glow); border: 1px solid var(--amber-dim);
        padding: 2px 8px; border-radius: 2px; display: inline-block; margin-bottom: 6px;
    }
    .ops-title { font-size: 1.75rem; font-weight: 700; color: var(--text) !important;
                 letter-spacing: -0.02em; margin: 0 0 4px 0; }
    .ops-sub   { color: var(--muted) !important; font-size: 0.85rem; margin: 0; }

    .stat-tile {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 6px; padding: 1rem 1.2rem;
        position: relative; overflow: hidden;
    }
    .stat-tile::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0;
        height: 2px; background: var(--amber);
    }
    .stat-tile.t::before  { background: var(--teal); }
    .stat-tile.r::before  { background: var(--red); }
    .stat-tile.g::before  { background: var(--green); }
    .stat-tile.m::before  { background: var(--border); }
    .stat-val { font-family: var(--mono); font-size: 1.85rem; font-weight: 600;
                color: var(--amber); line-height: 1; margin-bottom: 4px; }
    .stat-tile.t .stat-val { color: var(--teal); }
    .stat-tile.r .stat-val { color: var(--red); }
    .stat-tile.g .stat-val { color: var(--green); }
    .stat-tile.m .stat-val { color: var(--muted); }
    .stat-lbl  { font-size: 0.68rem; color: var(--muted); text-transform: uppercase;
                 letter-spacing: 0.1em; font-family: var(--mono); }

    .alert-bar {
        background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3);
        border-left: 3px solid var(--red); border-radius: 4px;
        padding: 0.75rem 1rem; margin-bottom: 1rem;
        font-family: var(--mono); font-size: 0.8rem; color: #fca5a5;
    }
    .warn-bar {
        background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25);
        border-left: 3px solid var(--amber); border-radius: 4px;
        padding: 0.75rem 1rem; margin-bottom: 1rem;
        font-family: var(--mono); font-size: 0.8rem; color: #fcd34d;
    }
    .ok-bar {
        background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.25);
        border-left: 3px solid var(--green); border-radius: 4px;
        padding: 0.75rem 1rem; margin-bottom: 1rem; font-size: 0.85rem; color: #86efac;
    }
    .badge {
        font-family: var(--mono); font-size: 0.65rem; padding: 2px 7px;
        border-radius: 2px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
    }
    .b-active    { background: rgba(34,197,94,0.12);  color: #86efac;  border: 1px solid rgba(34,197,94,0.25); }
    .b-refresh   { background: rgba(245,158,11,0.12); color: #fcd34d;  border: 1px solid rgba(245,158,11,0.25); }
    .b-retired   { background: rgba(100,116,139,0.12);color: #94a3b8;  border: 1px solid rgba(100,116,139,0.25); }
    .b-available { background: rgba(20,184,166,0.12); color: #5eead4;  border: 1px solid rgba(20,184,166,0.25); }
    .mono-tag {
        font-family: var(--mono); font-size: 0.72rem;
        background: var(--surface2); border: 1px solid var(--border);
        color: var(--dim); padding: 1px 6px; border-radius: 3px;
    }
    .section-label {
        font-family: var(--mono); font-size: 0.65rem; color: var(--amber);
        letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.75rem;
        padding-bottom: 0.4rem; border-bottom: 1px solid var(--border);
    }
    .chart-wrap {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 6px; padding: 1rem 1rem 0.5rem 1rem;
    }
    .tbl-header {
        font-family: var(--mono); font-size: 0.68rem; color: var(--muted);
        text-transform: uppercase; letter-spacing: 0.08em;
        padding: 0.5rem 0; border-bottom: 1px solid var(--border); margin-bottom: 0.4rem;
    }
    .asset-row {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 4px; padding: 0.55rem 0.8rem; margin-bottom: 3px;
        transition: border-color 0.12s;
    }
    .asset-row:hover { border-color: var(--amber); }
    .prio-c { color: #f87171; font-family: var(--mono); font-size: 0.75rem; font-weight: 600; }
    .prio-h { color: #fb923c; font-family: var(--mono); font-size: 0.75rem; font-weight: 600; }
    .prio-m { color: #fbbf24; font-family: var(--mono); font-size: 0.75rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.4rem 0 1.2rem 0; border-bottom:1px solid #2a2f3d; margin-bottom:1rem;'>
        <div style='font-family:IBM Plex Mono,monospace; font-size:0.62rem;
                    color:#f59e0b; letter-spacing:0.18em; text-transform:uppercase;
                    margin-bottom:5px;'>⬡ PLASMAN CORP</div>
        <div style='font-size:1rem; font-weight:700; color:#e2e8f0; letter-spacing:-0.01em;'>
            IT Asset Control
        </div>
        <div style='font-family:IBM Plex Mono,monospace; font-size:0.65rem;
                    color:#64748b; margin-top:3px;'>v1.0 · Windsor HQ</div>
    </div>
    """, unsafe_allow_html=True)

    nav = {
        "⬡  DASHBOARD":       "dashboard",
        "▦  INVENTORY":       "inventory",
        "↻  REFRESH PLANNER": "refresh",
        "↓  ONBOARDING":      "onboarding",
        "↑  OFFBOARDING":     "offboarding",
        "≡  TRANSITION LOG":  "log",
        "+  ADD ASSET":       "add_asset",
        "◎  AUDIT TRAIL":     "audit",
    }

    for label, key in nav.items():
        active = st.session_state.current_page == key
        if st.button(label, use_container_width=True,
                     type="primary" if active else "secondary", key=f"nav_{key}"):
            st.session_state.current_page = key
            st.rerun()

    st.markdown("""
    <div style='margin-top:1.5rem; padding-top:1rem; border-top:1px solid #2a2f3d;'>
        <div style='font-family:IBM Plex Mono,monospace; font-size:0.62rem;
                    color:#64748b; line-height:2;'>
            ASSETS ····· 75<br>
            LOCATIONS ·· 2<br>
            DEPTS ······ 8<br>
            ENGINE ····· SQLite
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

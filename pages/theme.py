THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

:root {
    --white:      #ffffff;
    --bg:         #f4f6f3;
    --bg2:        #eef1eb;
    --surface:    #ffffff;
    --border:     #e2e8da;
    --border2:    #d0d9c6;
    --green:      #2d6a4f;
    --green-lt:   #52b788;
    --green-xlt:  #d8f3dc;
    --green-glow: rgba(45,106,79,0.08);
    --slate:      #354f52;
    --slate-lt:   #84a98c;
    --coral:      #e76f51;
    --gold:       #e9c46a;
    --red:        #c1121f;
    --red-lt:     #ffddd2;
    --text:       #1a2e1d;
    --text2:      #3d5a42;
    --muted:      #6b7c6e;
    --mono:       'DM Mono', monospace;
    --shadow-sm:  0 1px 3px rgba(30,60,35,0.08), 0 1px 2px rgba(30,60,35,0.04);
    --shadow-md:  0 4px 12px rgba(30,60,35,0.1), 0 2px 4px rgba(30,60,35,0.06);
    --shadow-lg:  0 10px 30px rgba(30,60,35,0.12), 0 4px 10px rgba(30,60,35,0.08);
    --radius:     10px;
    --radius-sm:  6px;
    --radius-pill:99px;
}

/* ── APP SHELL ── */
.stApp { background: var(--bg) !important; }
[data-testid="stAppViewContainer"] { background: var(--bg) !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container {
    padding-top: 1.5rem !important;
    max-width: 100% !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--green) !important;
    border-right: none !important;
    box-shadow: 2px 0 20px rgba(30,60,35,0.15) !important;
}
[data-testid="stSidebar"] * { color: #d8f3dc !important; }
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid rgba(216,243,220,0.2) !important;
    color: rgba(216,243,220,0.75) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: var(--radius-sm) !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(216,243,220,0.12) !important;
    border-color: rgba(216,243,220,0.4) !important;
    color: #d8f3dc !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: rgba(216,243,220,0.18) !important;
    border-color: rgba(216,243,220,0.5) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── GLOBAL TEXT ── */
p, li, label, div { color: var(--text); }
h1,h2,h3,h4 { color: var(--text) !important; font-family: 'DM Sans', sans-serif; font-weight: 700; }

/* ── INPUTS ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    box-shadow: var(--shadow-sm) !important;
    transition: border-color 0.2s !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus {
    border-color: var(--green-lt) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.15) !important;
}

/* ── LABELS ── */
[data-testid="stWidgetLabel"] p {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: var(--muted) !important;
}

/* ── BUTTONS ── */
.stButton button {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text2) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    border-color: var(--green-lt) !important;
    color: var(--green) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}
.stButton button[kind="primary"] {
    background: var(--green) !important;
    border-color: var(--green) !important;
    color: #fff !important;
    box-shadow: 0 4px 14px rgba(45,106,79,0.35) !important;
}
.stButton button[kind="primary"]:hover {
    background: #236140 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(45,106,79,0.4) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    overflow: hidden !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── FORM ── */
[data-testid="stForm"] {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-md) !important;
    padding: 1.5rem !important;
}

/* ── DOWNLOAD ── */
.stDownloadButton button {
    background: var(--green-xlt) !important;
    border: 1.5px solid var(--green-lt) !important;
    color: var(--green) !important;
    font-weight: 600 !important;
}

/* ── MULTISELECT ── */
[data-testid="stMultiSelect"] > div {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: var(--green-xlt) !important;
    color: var(--green) !important;
    border-radius: var(--radius-pill) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--slate-lt); }

/* ── CUSTOM COMPONENTS ── */

.page-header {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-sm);
    border: 1.5px solid var(--border);
    display: flex;
    align-items: center;
    gap: 1rem;
}
.page-header-icon {
    width: 48px; height: 48px;
    background: var(--green-xlt);
    border-radius: var(--radius);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
}
.page-header-text .eyebrow {
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--green-lt); margin-bottom: 2px;
}
.page-header-text h1 {
    font-size: 1.5rem !important; font-weight: 700 !important;
    color: var(--text) !important; margin: 0 0 2px 0 !important; line-height: 1.2;
}
.page-header-text p { color: var(--muted) !important; font-size: 0.85rem; margin: 0; }

.kpi-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.1rem 1.25rem;
    box-shadow: var(--shadow-sm);
    border: 1.5px solid var(--border);
    transition: box-shadow 0.2s, transform 0.2s;
}
.kpi-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.kpi-card .kpi-icon {
    width: 36px; height: 36px; border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; margin-bottom: 10px;
}
.kpi-card .kpi-val {
    font-size: 2rem; font-weight: 700; color: var(--text);
    line-height: 1; margin-bottom: 3px;
    font-family: 'DM Mono', monospace;
}
.kpi-card .kpi-lbl {
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.07em; color: var(--muted);
}
.kpi-card .kpi-sub {
    font-size: 0.72rem; color: var(--muted); margin-top: 6px;
    padding-top: 6px; border-top: 1px solid var(--border);
}

.alert-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fff4f4; border: 1.5px solid #fecaca;
    border-radius: var(--radius-pill); padding: 6px 14px;
    font-size: 0.8rem; font-weight: 600; color: var(--red);
    margin-bottom: 1rem;
}
.warn-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fffbeb; border: 1.5px solid #fde68a;
    border-radius: var(--radius-pill); padding: 6px 14px;
    font-size: 0.8rem; font-weight: 600; color: #92400e;
    margin-bottom: 1rem;
}
.ok-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--green-xlt); border: 1.5px solid #b7e4c7;
    border-radius: var(--radius-pill); padding: 6px 14px;
    font-size: 0.8rem; font-weight: 600; color: var(--green);
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.05em;
    padding: 3px 10px; border-radius: var(--radius-pill);
}
.b-active    { background: #d8f3dc; color: #1b4332; }
.b-refresh   { background: #fef3c7; color: #78350f; }
.b-retired   { background: #f1f5f9; color: #475569; }
.b-available { background: #dbeafe; color: #1e3a8a; }
.b-critical  { background: #fee2e2; color: #991b1b; }
.b-high      { background: #ffedd5; color: #9a3412; }
.b-medium    { background: #fef9c3; color: #713f12; }

.asset-card {
    background: var(--white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 0.9rem 1.1rem;
    margin-bottom: 6px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.15s, border-color 0.15s, transform 0.15s;
}
.asset-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--green-lt);
    transform: translateY(-1px);
}

.section-head {
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--muted); margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

.edit-panel {
    background: linear-gradient(135deg, #f0faf4 0%, #ffffff 100%);
    border: 2px solid var(--green-lt);
    border-radius: var(--radius);
    padding: 1.4rem;
    margin-top: 1rem;
    box-shadow: 0 0 0 4px rgba(82,183,136,0.1);
}

.info-row {
    background: var(--bg);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}

.mono { font-family: var(--mono); font-size: 0.8rem; }

.chart-card {
    background: var(--white);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1rem 0.5rem 1rem;
    box-shadow: var(--shadow-sm);
}

.transition-card {
    background: var(--white);
    border: 1.5px solid var(--border);
    border-left: 4px solid var(--green-lt);
    border-radius: var(--radius);
    padding: 0.9rem 1.1rem;
    margin-bottom: 6px;
    box-shadow: var(--shadow-sm);
}
.transition-card.off {
    border-left-color: var(--coral);
}

.action-plan-row {
    display: flex; align-items: center; gap: 12px;
    padding: 0.8rem 1rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
}
.action-plan-row:last-child { border-bottom: none; }

.tbl-col-head {
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--muted);
}
</style>
"""

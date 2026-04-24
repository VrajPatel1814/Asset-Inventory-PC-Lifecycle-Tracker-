# 🖥️ IT Asset Inventory & PC Lifecycle Tracker

A full-stack IT asset management system built with Python and Streamlit.
Tracks 75+ devices across departments and locations, with automated PC refresh alerts,
onboarding/offboarding workflows, and audit-ready reporting.

---

## 📸 Features

### 📊 Dashboard
- 6 live KPI cards (total assets, active, needs refresh, retired, by location)
- 5 visual panels: status breakdown, device type, department, location, age distribution
- Auto-flagging banner when refresh candidates exist
- Top 10 oldest devices table

### 🖥️ Asset Inventory
- Full searchable, filterable table of all 75+ assets
- Filters: status, department, device type, location, keyword search
- Inline edit panel — update assignment, status, location, notes
- Retire asset with one click
- Export to CSV

### 🔄 PC Refresh Planner
- Automatically flags all devices older than 3 years
- Priority scoring: Medium (3–4 yrs) → High (4–5 yrs) → Critical (5+ yrs)
- Charts by department and device type
- Colour-coded refresh table with export
- Action plan recommendation table

### 👤 Onboarding
- Assign available equipment to new employees
- Auto-updates asset status and assignment
- Saves to onboarding log

### 📤 Offboarding
- View all assets assigned to a departing employee
- Return selected equipment (status → Available for redeployment)
- Saves to offboarding log

### 📋 Onboarding & Offboarding Log
- Full transition history with export to CSV
- Audit-ready documentation

### ➕ Add New Asset
- Register any new device with auto-generated asset ID

### 📁 Audit Trail
- Every asset update and retirement is logged with timestamp and actor

---

## 🚀 Running Locally

```bash
git clone https://github.com/VrajPatel1814/it-asset-inventory-tracker
cd it-asset-inventory-tracker
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New app → select repo → main file: `app.py` → Deploy

---

## 🗂️ Project Structure

```
it-asset-inventory-tracker/
├── app.py                  # Entry point, sidebar, page router
├── database.py             # SQLite DB, 75 seeded assets, all queries
├── requirements.txt
├── pages/
│   ├── dashboard.py        # KPI cards + 5 Plotly charts
│   ├── inventory.py        # Full asset table with inline edit
│   ├── refresh.py          # PC refresh planner with priority scoring
│   ├── onboarding.py       # New employee equipment assignment
│   ├── offboarding.py      # Equipment return workflow
│   ├── ob_log.py           # Onboarding/offboarding log
│   ├── add_asset.py        # Register new device
│   └── audit.py            # Full audit trail
└── data/
    └── assets.db           # SQLite database (auto-created on first run)
```

---

## 📊 Sample Data

Pre-loaded with **75 realistic assets** across:
- 4 device types: Laptop, Desktop, Monitor, Mobile Device
- 3 statuses: Active, Needs Refresh, Retired
- 8 departments: Finance, HR, IT, Operations, Sales, Accounting, Engineering, Quality, Marketing
- 2 locations: Windsor HQ & Plant Floor
- 18 devices flagged for refresh (24% of inventory)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** SQLite
- **Charts:** Plotly Express
- **Deployment:** Streamlit Cloud

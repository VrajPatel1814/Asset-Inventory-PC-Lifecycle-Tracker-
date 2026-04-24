import sqlite3
import os
from datetime import datetime, date
import csv
import io

DB_PATH = "data/assets.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT UNIQUE NOT NULL,
            device_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            serial_number TEXT UNIQUE NOT NULL,
            assigned_to TEXT NOT NULL,
            department TEXT NOT NULL,
            location TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            notes TEXT DEFAULT ''
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS onboarding_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_type TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            department TEXT NOT NULL,
            asset_ids TEXT NOT NULL,
            processed_by TEXT NOT NULL,
            processed_at TEXT NOT NULL,
            notes TEXT DEFAULT ''
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT NOT NULL,
            action TEXT NOT NULL,
            changed_by TEXT NOT NULL,
            changed_at TEXT NOT NULL,
            details TEXT DEFAULT ''
        )
    """)

    conn.commit()

    c.execute("SELECT COUNT(*) FROM assets")
    if c.fetchone()[0] == 0:
        seed_data(conn)

    conn.close()


def seed_data(conn):
    c = conn.cursor()

    employees = [
        ("James Carter",     "james.carter@plasman.com",    "Finance",     "Windsor HQ",  "Active"),
        ("Sarah Mitchell",   "sarah.mitchell@plasman.com",  "HR",          "Windsor HQ",  "Active"),
        ("Omar Farouk",      "omar.farouk@plasman.com",     "IT",          "Windsor HQ",  "Active"),
        ("Priya Sharma",     "priya.sharma@plasman.com",    "Operations",  "Plant Floor", "Active"),
        ("Tom Nguyen",       "tom.nguyen@plasman.com",      "Sales",       "Windsor HQ",  "Active"),
        ("Linda Zhao",       "linda.zhao@plasman.com",      "Accounting",  "Windsor HQ",  "Active"),
        ("Kevin Brown",      "kevin.brown@plasman.com",     "Engineering", "Plant Floor", "Active"),
        ("Fatima Al-Hassan", "fatima.alhassan@plasman.com", "IT",          "Windsor HQ",  "Active"),
        ("Amy Chen",         "amy.chen@plasman.com",        "Marketing",   "Windsor HQ",  "Active"),
        ("David Park",       "david.park@plasman.com",      "Engineering", "Plant Floor", "Active"),
        ("Rachel Green",     "rachel.green@plasman.com",    "Finance",     "Windsor HQ",  "Active"),
        ("Marcus Johnson",   "marcus.johnson@plasman.com",  "Quality",     "Plant Floor", "Active"),
        ("Julia Thompson",   "julia.thompson@plasman.com",  "HR",          "Windsor HQ",  "Active"),
        ("Carlos Rivera",    "carlos.rivera@plasman.com",   "Operations",  "Plant Floor", "Active"),
        ("Mei Lin",          "mei.lin@plasman.com",         "Finance",     "Windsor HQ",  "Active"),
        ("George Murphy",    "george.murphy@plasman.com",   "Quality",     "Plant Floor", "Active"),
        ("Sophie Turner",    "sophie.turner@plasman.com",   "Marketing",   "Windsor HQ",  "Active"),
        ("Hassan Ali",       "hassan.ali@plasman.com",      "Accounting",  "Windsor HQ",  "Active"),
        ("Ryan Patel",       "ryan.patel@plasman.com",      "Engineering", "Plant Floor", "Active"),
        ("Diane Foster",     "diane.foster@plasman.com",    "Finance",     "Windsor HQ",  "Active"),
    ]
    c.executemany(
        "INSERT INTO employees (name, email, department, location, status) VALUES (?, ?, ?, ?, ?)",
        employees
    )

    assets_csv = """asset_id,device_type,brand,model,serial_number,assigned_to,department,location,purchase_date,status
A001,Laptop,Dell,Latitude 5540,DL-XK9281,James Carter,Finance,Windsor HQ,2021-03-15,Active
A002,Laptop,Lenovo,ThinkPad E15,LN-QP4472,Sarah Mitchell,HR,Windsor HQ,2020-07-22,Needs Refresh
A003,Desktop,HP,EliteDesk 800,HP-RN7734,Omar Farouk,IT,Windsor HQ,2022-11-01,Active
A004,Laptop,Dell,Latitude 5540,DL-BV2209,Priya Sharma,Operations,Plant Floor,2019-05-10,Needs Refresh
A005,Monitor,LG,27UK850,LG-TT8821,James Carter,Finance,Windsor HQ,2021-03-15,Active
A006,Laptop,HP,ProBook 450,HP-CC1193,Tom Nguyen,Sales,Windsor HQ,2023-01-18,Active
A007,Desktop,Dell,OptiPlex 7090,DL-MM5567,Linda Zhao,Accounting,Windsor HQ,2020-09-30,Needs Refresh
A008,Laptop,Lenovo,ThinkPad T14,LN-DD3341,Kevin Brown,Engineering,Plant Floor,2022-06-14,Active
A009,Mobile Device,Apple,iPhone 13,AP-WW6612,Sarah Mitchell,HR,Windsor HQ,2022-08-05,Active
A010,Laptop,Dell,Latitude 5540,DL-PP9934,Fatima Al-Hassan,IT,Windsor HQ,2021-12-20,Active
A011,Desktop,HP,EliteDesk 600,HP-ZZ4423,Carlos Rivera,Operations,Plant Floor,2019-02-14,Retired
A012,Laptop,HP,ProBook 440,HP-LL8872,Amy Chen,Marketing,Windsor HQ,2023-03-11,Active
A013,Monitor,Dell,P2422H,DL-MN2234,Omar Farouk,IT,Windsor HQ,2022-11-01,Active
A014,Laptop,Lenovo,ThinkPad L15,LN-KK7765,David Park,Engineering,Plant Floor,2020-04-19,Needs Refresh
A015,Desktop,Dell,OptiPlex 5090,DL-SS1198,Rachel Green,Finance,Windsor HQ,2023-07-07,Active
A016,Mobile Device,Samsung,Galaxy S22,SM-BB4456,Tom Nguyen,Sales,Windsor HQ,2022-09-23,Active
A017,Laptop,Dell,Latitude 3540,DL-GG7713,Marcus Johnson,Quality,Plant Floor,2021-08-30,Active
A018,Desktop,Lenovo,ThinkCentre M70,LN-HH2287,Linda Zhao,Accounting,Windsor HQ,2019-11-05,Needs Refresh
A019,Laptop,HP,EliteBook 840,HP-FF5541,Julia Thompson,HR,Windsor HQ,2022-02-17,Active
A020,Monitor,HP,24mh FHD,HP-MN9934,Linda Zhao,Accounting,Windsor HQ,2020-09-30,Active
A021,Laptop,Dell,Latitude 5540,DL-RR3376,Omar Farouk,IT,Windsor HQ,2023-05-22,Active
A022,Desktop,HP,EliteDesk 800,HP-QQ6619,Priya Sharma,Operations,Plant Floor,2021-01-13,Active
A023,Laptop,Lenovo,ThinkPad E14,LN-VV8834,Tom Nguyen,Sales,Windsor HQ,2020-06-08,Needs Refresh
A024,Mobile Device,Apple,iPhone 14,AP-CC3378,Kevin Brown,Engineering,Plant Floor,2023-01-09,Active
A025,Laptop,HP,ProBook 450,HP-JJ4456,Mei Lin,Finance,Windsor HQ,2022-10-25,Active
A026,Desktop,Dell,OptiPlex 7090,DL-AA5523,George Murphy,Quality,Plant Floor,2021-04-16,Active
A027,Monitor,LG,24MK430,LG-MN1123,Carlos Rivera,Operations,Plant Floor,2022-05-30,Active
A028,Laptop,Dell,Latitude 3540,DL-NN8867,Sophie Turner,Marketing,Windsor HQ,2019-08-21,Needs Refresh
A029,Desktop,Lenovo,ThinkCentre M80,LN-PP2245,Hassan Ali,Accounting,Windsor HQ,2023-09-14,Active
A030,Laptop,HP,EliteBook 850,HP-TT7712,Julia Thompson,HR,Windsor HQ,2022-07-03,Active
A031,Mobile Device,Samsung,Galaxy S21,SM-DD9901,Amy Chen,Marketing,Windsor HQ,2021-06-17,Active
A032,Laptop,Lenovo,ThinkPad T15,LN-EE6634,Ryan Patel,Engineering,Plant Floor,2020-12-29,Needs Refresh
A033,Desktop,HP,EliteDesk 600,HP-WW3312,Diane Foster,Finance,Windsor HQ,2022-03-08,Active
A034,Monitor,Dell,P2722H,DL-MN8856,Priya Sharma,Operations,Plant Floor,2022-06-14,Active
A035,Laptop,Dell,Latitude 5540,DL-UU1167,Omar Farouk,IT,Windsor HQ,2023-11-19,Active
A036,Desktop,Dell,OptiPlex 5090,DL-YY4490,Marcus Johnson,Quality,Plant Floor,2021-10-05,Active
A037,Laptop,HP,ProBook 430,HP-BB8823,Tom Nguyen,Sales,Windsor HQ,2020-01-14,Needs Refresh
A038,Mobile Device,Apple,iPhone 12,AP-GG5567,Marcus Johnson,Quality,Plant Floor,2021-03-22,Needs Refresh
A039,Laptop,Lenovo,ThinkPad L14,LN-SS9978,Julia Thompson,HR,Windsor HQ,2022-04-11,Active
A040,Desktop,HP,EliteDesk 800,HP-NN6645,Hassan Ali,Accounting,Windsor HQ,2019-07-30,Retired
A041,Laptop,Dell,Latitude 3540,DL-MM4401,Sophie Turner,Marketing,Windsor HQ,2023-02-28,Active
A042,Monitor,HP,27f FHD,HP-MN3378,Rachel Green,Finance,Windsor HQ,2023-07-07,Active
A043,Desktop,Lenovo,ThinkCentre M70,LN-RR7756,Ryan Patel,Engineering,Plant Floor,2020-08-18,Needs Refresh
A044,Laptop,HP,EliteBook 840,HP-KK1134,Fatima Al-Hassan,IT,Windsor HQ,2022-12-06,Active
A045,Mobile Device,Samsung,Galaxy S23,SM-HH2290,Tom Nguyen,Sales,Windsor HQ,2023-06-15,Active
A046,Laptop,Dell,Latitude 5540,DL-CC6689,Carlos Rivera,Operations,Plant Floor,2021-07-24,Active
A047,Desktop,HP,EliteDesk 600,HP-FF9923,Diane Foster,Finance,Windsor HQ,2022-09-01,Active
A048,Monitor,LG,27MK600,LG-MN4467,David Park,Engineering,Plant Floor,2020-04-19,Active
A049,Laptop,Lenovo,ThinkPad E15,LN-LL3312,George Murphy,Quality,Plant Floor,2023-08-30,Active
A050,Desktop,Dell,OptiPlex 7090,DL-ZZ8878,Hassan Ali,Accounting,Windsor HQ,2021-05-12,Active
A051,Laptop,HP,ProBook 450,HP-AA4467,Julia Thompson,HR,Windsor HQ,2020-10-07,Needs Refresh
A052,Mobile Device,Apple,iPhone 14,AP-VV1145,Diane Foster,Finance,Windsor HQ,2022-11-28,Active
A053,Laptop,Dell,Latitude 3540,DL-TT5534,Omar Farouk,IT,Windsor HQ,2023-04-17,Active
A054,Desktop,Lenovo,ThinkCentre M80,LN-WW8823,Linda Zhao,Accounting,Windsor HQ,2022-06-20,Active
A055,Monitor,Dell,P2422H,DL-MN6612,Sophie Turner,Marketing,Windsor HQ,2023-02-28,Active
A056,Laptop,HP,EliteBook 850,HP-DD2256,Tom Nguyen,Sales,Windsor HQ,2021-11-09,Active
A057,Desktop,HP,EliteDesk 800,HP-EE7789,David Park,Engineering,Plant Floor,2019-04-03,Retired
A058,Laptop,Lenovo,ThinkPad T14,LN-BB5512,Carlos Rivera,Operations,Plant Floor,2022-08-16,Active
A059,Mobile Device,Samsung,Galaxy S22,SM-PP3367,George Murphy,Quality,Plant Floor,2022-10-04,Active
A060,Laptop,Dell,Latitude 5540,DL-HH9956,Diane Foster,Finance,Windsor HQ,2023-10-11,Active
A061,Desktop,Dell,OptiPlex 5090,DL-II4423,Julia Thompson,HR,Windsor HQ,2021-09-27,Active
A062,Monitor,HP,24mh FHD,HP-MN5589,Ryan Patel,Engineering,Plant Floor,2020-08-18,Active
A063,Laptop,HP,ProBook 440,HP-GG3378,Amy Chen,Marketing,Windsor HQ,2022-01-24,Active
A064,Desktop,Lenovo,ThinkCentre M70,LN-JJ6634,Hassan Ali,Accounting,Windsor HQ,2020-03-15,Needs Refresh
A065,Laptop,Dell,Latitude 3540,DL-OO7701,Omar Farouk,IT,Windsor HQ,2023-06-03,Active
A066,Mobile Device,Apple,iPhone 13,AP-LL4478,Tom Nguyen,Sales,Windsor HQ,2021-11-09,Active
A067,Laptop,Lenovo,ThinkPad L15,LN-XX9912,Fatima Al-Hassan,IT,Windsor HQ,2022-05-18,Active
A068,Desktop,HP,EliteDesk 600,HP-YY2256,Carlos Rivera,Operations,Plant Floor,2023-03-29,Active
A069,Monitor,LG,27UK850,LG-MN8890,Diane Foster,Finance,Windsor HQ,2023-10-11,Active
A070,Laptop,HP,EliteBook 840,HP-MM1123,Marcus Johnson,Quality,Plant Floor,2021-02-08,Active
A071,Desktop,Dell,OptiPlex 7090,DL-NN3389,Hassan Ali,Accounting,Windsor HQ,2022-07-19,Active
A072,Laptop,Dell,Latitude 5540,DL-QQ6656,David Park,Engineering,Plant Floor,2020-11-23,Needs Refresh
A073,Mobile Device,Samsung,Galaxy S23,SM-RR7734,Julia Thompson,HR,Windsor HQ,2023-05-07,Active
A074,Laptop,Lenovo,ThinkPad E14,LN-SS4401,Tom Nguyen,Sales,Windsor HQ,2022-03-14,Active
A075,Desktop,HP,EliteDesk 800,HP-UU8867,David Park,Engineering,Plant Floor,2023-08-22,Active"""

    reader = csv.DictReader(io.StringIO(assets_csv))
    for row in reader:
        c.execute("""
            INSERT INTO assets (asset_id, device_type, brand, model, serial_number,
                assigned_to, department, location, purchase_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["asset_id"], row["device_type"], row["brand"], row["model"],
            row["serial_number"], row["assigned_to"], row["department"],
            row["location"], row["purchase_date"], row["status"]
        ))

    conn.commit()


# ── ASSET QUERIES ────────────────────────────────────────────────

def get_all_assets(status_filter=None, dept_filter=None, type_filter=None, location_filter=None):
    conn   = get_connection()
    query  = "SELECT * FROM assets WHERE 1=1"
    params = []
    if status_filter   and status_filter   != "All": query += " AND status=?";      params.append(status_filter)
    if dept_filter     and dept_filter     != "All": query += " AND department=?";  params.append(dept_filter)
    if type_filter     and type_filter     != "All": query += " AND device_type=?"; params.append(type_filter)
    if location_filter and location_filter != "All": query += " AND location=?";    params.append(location_filter)
    query += " ORDER BY asset_id"
    assets = conn.execute(query, params).fetchall()
    conn.close()
    return assets

def get_asset_by_id(asset_id):
    conn  = get_connection()
    asset = conn.execute("SELECT * FROM assets WHERE asset_id=?", (asset_id,)).fetchone()
    conn.close()
    return asset

def add_asset(asset_id, device_type, brand, model, serial_number,
              assigned_to, department, location, purchase_date, status, notes=""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO assets (asset_id, device_type, brand, model, serial_number,
            assigned_to, department, location, purchase_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (asset_id, device_type, brand, model, serial_number,
          assigned_to, department, location, purchase_date, status, notes))
    conn.commit()
    conn.close()

def update_asset(asset_id, assigned_to, department, location, status, notes, changed_by):
    conn = get_connection()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        UPDATE assets SET assigned_to=?, department=?, location=?,
            status=?, notes=? WHERE asset_id=?
    """, (assigned_to, department, location, status, notes, asset_id))
    conn.execute("""
        INSERT INTO audit_log (asset_id, action, changed_by, changed_at, details)
        VALUES (?, 'Updated', ?, ?, ?)
    """, (asset_id, changed_by, now, f"Status→{status}, Assigned→{assigned_to}"))
    conn.commit()
    conn.close()

def retire_asset(asset_id, changed_by):
    conn = get_connection()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("UPDATE assets SET status='Retired' WHERE asset_id=?", (asset_id,))
    conn.execute("""
        INSERT INTO audit_log (asset_id, action, changed_by, changed_at, details)
        VALUES (?, 'Retired', ?, ?, 'Asset marked as retired')
    """, (asset_id, changed_by, now))
    conn.commit()
    conn.close()

def get_refresh_candidates(years=3):
    conn       = get_connection()
    cutoff     = date.today().replace(year=date.today().year - years).isoformat()
    candidates = conn.execute("""
        SELECT * FROM assets
        WHERE purchase_date <= ? AND status != 'Retired'
        ORDER BY purchase_date ASC
    """, (cutoff,)).fetchall()
    conn.close()
    return candidates

def get_audit_log(asset_id=None):
    conn  = get_connection()
    if asset_id:
        logs = conn.execute(
            "SELECT * FROM audit_log WHERE asset_id=? ORDER BY changed_at DESC", (asset_id,)
        ).fetchall()
    else:
        logs = conn.execute(
            "SELECT * FROM audit_log ORDER BY changed_at DESC LIMIT 100"
        ).fetchall()
    conn.close()
    return logs

# ── EMPLOYEE QUERIES ─────────────────────────────────────────────

def get_all_employees():
    conn      = get_connection()
    employees = conn.execute("SELECT * FROM employees ORDER BY name").fetchall()
    conn.close()
    return employees

def get_assets_by_employee(name):
    conn   = get_connection()
    assets = conn.execute(
        "SELECT * FROM assets WHERE assigned_to=? AND status != 'Retired'", (name,)
    ).fetchall()
    conn.close()
    return assets

# ── ONBOARDING / OFFBOARDING ─────────────────────────────────────

def log_onboarding(employee_name, department, asset_ids, processed_by, notes=""):
    conn = get_connection()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO onboarding_log (log_type, employee_name, department, asset_ids,
            processed_by, processed_at, notes)
        VALUES ('Onboarding', ?, ?, ?, ?, ?, ?)
    """, (employee_name, department, ", ".join(asset_ids), processed_by, now, notes))
    conn.commit()
    conn.close()

def log_offboarding(employee_name, department, asset_ids, processed_by, notes=""):
    conn = get_connection()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO onboarding_log (log_type, employee_name, department, asset_ids,
            processed_by, processed_at, notes)
        VALUES ('Offboarding', ?, ?, ?, ?, ?, ?)
    """, (employee_name, department, ", ".join(asset_ids), processed_by, now, notes))
    for aid in asset_ids:
        conn.execute(
            "UPDATE assets SET assigned_to='Unassigned', status='Available' WHERE asset_id=?", (aid,)
        )
    conn.commit()
    conn.close()

def get_onboarding_log():
    conn = get_connection()
    logs = conn.execute(
        "SELECT * FROM onboarding_log ORDER BY processed_at DESC"
    ).fetchall()
    conn.close()
    return logs

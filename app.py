import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, start_date TEXT, date TEXT, amount REAL)")

    c.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        amount REAL,
        interest_rate REAL,
        start_date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS loan_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_id INTEGER,
        amount REAL,
        date TEXT
    )
    """)

    c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")

    conn.commit()

create_tables()

# ===== FIX columns =====
def safe_add_customer_start_date():
    try:
        c.execute("ALTER TABLE customers ADD COLUMN start_date TEXT")
    except:
        pass

safe_add_customer_start_date()

def safe_add_column(table, column):
    try:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")
    except:
        pass

safe_add_column("donations", "date")
safe_add_column("expenses", "date")

# ===== PASSWORD =====
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ===== DEFAULT ADMIN =====
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users VALUES (?,?,?)", ("admin", hash_pass("admin123"), "Admin"))
    conn.commit()

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva SaaS", layout="wide")

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, hash_pass(p))
        ).fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user[0]
            st.session_state.role = user[2]
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ===== ROLE FLAGS =====
role = st.session_state.role
is_admin = role == "Admin"
is_editor = role == "Editor"
is_viewer = role == "Viewer"

# ================= MENU =================
with st.sidebar:
    st.markdown("## 🚀 Bal Yuva SaaS")
    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","loans","Donations","Expenses","Reports","Users","AI"],
        icons=["house","people","cash","bank","gift","credit-card","bar-chart","person","robot"],
        default_index=0,
    )

# ================= USER BAR =================
col_user, col_logout = st.columns([3,1])
with col_user:
    st.write(f"👤 {st.session_state.current_user}")
with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("---")

# ================= DASHBOARD =================
if menu == "Dashboard":

    total_col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    total_loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0
    total_don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    total_exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("loans", f"₹ {total_loan}")
    c3.metric("Donations", f"₹ {total_don}")
    c4.metric("Expenses", f"₹ {total_exp}")
    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# ================= CUSTOMERS =================
elif menu == "Customers":

    st.subheader("👤 Customer Management")

    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile")
    start_date = st.date_input("Start Date")

    if not is_viewer:
        if st.button("Add Customer"):
            c.execute("INSERT INTO customers VALUES (?,?,?)",
                      (name, mobile, start_date.strftime("%Y-%m-%d")))
            conn.commit()
            st.success("Added")
            st.rerun()

    df = pd.read_sql("SELECT rowid as id, * FROM customers", conn)
    st.dataframe(df)

# ================= COLLECTION =================
elif menu == "Collections":

    st.subheader("🔥 Collection Management")

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:
        cust = st.selectbox("Customer", customers["name"])
        month = st.selectbox("Month", [datetime.date(2026, m, 1).strftime("%B %Y") for m in range(1,13)])
        date = st.date_input("Date")
        amt = st.number_input("Amount")

        if not is_viewer:
            if st.button("Save"):
                start_date = customers[customers["name"]==cust]["start_date"].values[0]
                c.execute("INSERT INTO collections VALUES (?,?,?,?,?)",
                          (cust, month, start_date, date.strftime("%Y-%m-%d"), amt))
                conn.commit()
                st.success("Saved")
                st.rerun()

    st.dataframe(pd.read_sql("SELECT * FROM collections", conn))

# ================= LOANS =================
elif menu == "loans":

    st.subheader("💰 Loan Management")

    customers = pd.read_sql("SELECT * FROM customers", conn)
    loans_df = pd.read_sql("SELECT * FROM loans", conn)

    if not customers.empty:
        cust = st.selectbox("Customer", customers["name"])
        amt = st.number_input("Loan Amount")

        if not is_viewer:
            if st.button("Add Loan"):
                c.execute("INSERT INTO loans (customer_name,amount) VALUES (?,?)",(cust,amt))
                conn.commit()
                st.success("Loan Added")
                st.rerun()

    st.dataframe(loans_df)

# ================= DONATIONS =================
elif menu == "Donations":

    if not is_viewer:
        name = st.text_input("Name")
        amt = st.number_input("Amount")

        if st.button("Save"):
            c.execute("INSERT INTO donations VALUES (?,?,date('now'))",(name,amt))
            conn.commit()
            st.success("Saved")
            st.rerun()

    st.dataframe(pd.read_sql("SELECT * FROM donations", conn))

# ================= EXPENSES =================
elif menu == "Expenses":

    if not is_viewer:
        name = st.text_input("Type")
        amt = st.number_input("Amount")

        if st.button("Save"):
            c.execute("INSERT INTO expenses VALUES (?,?,date('now'))",(name,amt))
            conn.commit()
            st.success("Saved")
            st.rerun()

    st.dataframe(pd.read_sql("SELECT * FROM expenses", conn))

# ================= USERS =================
elif menu == "Users":

    if not is_admin:
        st.warning("Admin only")
    else:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        r = st.selectbox("Role", ["Admin","Editor","Viewer"])

        if st.button("Create"):
            c.execute("INSERT INTO users VALUES (?,?,?)",(u,hash_pass(p),r))
            conn.commit()
            st.success("Created")

        st.dataframe(pd.read_sql("SELECT username, role FROM users", conn))

# ================= AI =================
elif menu == "AI":
    st.info("Coming Soon")

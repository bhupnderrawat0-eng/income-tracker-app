import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import sqlite3
import datetime

# ================= DATABASE =================
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, date TEXT, amount REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS loans(name TEXT, date TEXT, amount REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL)")
    conn.commit()

create_tables()

# ================= HASH =================
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# Default admin
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users VALUES (?,?,?)", ("admin", hash_pass("admin123"), "Admin"))
    conn.commit()

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva SaaS", layout="wide")

# ================= LOGIN =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hash_pass(p)

        user = c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hashed)).fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user[0]
            st.session_state.role = user[2]
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🚀 Bal Yuva SaaS")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users"]
    )

    st.write("---")
    st.write(st.session_state.current_user)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================= HEADER =================
st.markdown("""
<div style="background:rgba(0,0,0,0.4);padding:15px;border-radius:12px;margin-bottom:20px;">
<h2 style='color:white;'>🚀 Bal Yuva Mangal Dal</h2>
<p style='color:lightgray;'>Smart Finance SaaS System</p>
</div>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================
if menu == "Dashboard":

    total_col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    total_loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0
    total_don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    total_exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("Loans", f"₹ {total_loan}")
    c3.metric("Donations", f"₹ {total_don}")
    c4.metric("Expenses", f"₹ {total_exp}")

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# ================= CUSTOMERS =================
elif menu == "Customers":

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        c.execute("INSERT INTO customers VALUES (?,?)",(name,mobile))
        conn.commit()

    df = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df)

# ================= COLLECTION =================
elif menu == "Collections":

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:

        cust = st.selectbox("Customer", customers["name"])

        month = st.selectbox("Month",
            [datetime.date(2026,m,1).strftime("%B %Y") for m in range(1,13)]
        )

        date = st.date_input("Date")
        amt = st.number_input("Amount")

        if st.button("Save Collection"):
            c.execute("INSERT INTO collections VALUES (?,?,?,?)",(cust,month,str(date),amt))
            conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM collections", conn))

# ================= LOANS =================
elif menu == "Loans":

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:

        cust = st.selectbox("Customer", customers["name"])
        date = st.date_input("Date")
        amt = st.number_input("Amount")

        if st.button("Add Loan"):
            c.execute("INSERT INTO loans VALUES (?,?,?)",(cust,str(date),amt))
            conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM loans", conn))

# ================= DONATIONS =================
elif menu == "Donations":

    donor = st.text_input("Donor Name")
    amt = st.number_input("Amount")

    if st.button("Save Donation"):
        c.execute("INSERT INTO donations VALUES (?,?)",(donor,amt))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM donations", conn))

# ================= EXPENSES =================
elif menu == "Expenses":

    exp = st.text_input("Expense Type")
    amt = st.number_input("Amount")

    if st.button("Save Expense"):
        c.execute("INSERT INTO expenses VALUES (?,?)",(exp,amt))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM expenses", conn))

# ================= REPORT =================
elif menu == "Reports":

    df = pd.DataFrame({
        "Category":["Collections","Loans","Donations","Expenses"],
        "Amount":[
            c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
        ]
    })

    st.bar_chart(df.set_index("Category"))

# ================= USERS =================
elif menu == "Users":

    if st.session_state.role != "Admin":
        st.warning("Only Admin Access")
    else:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        r = st.selectbox("Role", ["Admin","Editor","Viewer"])

        if st.button("Create User"):
            c.execute("INSERT INTO users VALUES (?,?,?)",(u,hash_pass(p),r))
            conn.commit()
            st.success("User Created")

        st.dataframe(pd.read_sql("SELECT username, role FROM users", conn))

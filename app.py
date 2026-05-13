import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu
import hashlib
import datetime

# =====================================
# DATABASE
# =====================================
conn = sqlite3.connect("finance.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
(name TEXT, password TEXT, role TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS customers
(name TEXT, mobile TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS collections
(name TEXT, mobile TEXT, month TEXT, date TEXT, amount REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS loans
(name TEXT, mobile TEXT, date TEXT, amount REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS donations
(name TEXT, amount REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS expenses
(type TEXT, amount REAL)''')

conn.commit()

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(page_title="Finance Pro", layout="wide")

# =====================================
# LOGIN
# =====================================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        enc = hashlib.sha256(pwd.encode()).hexdigest()

        data = c.execute("SELECT * FROM users WHERE name=? AND password=?", (user, enc)).fetchone()

        if data:
            st.session_state.login = True
            st.session_state.user = user
            st.session_state.role = data[2]
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:

    st.markdown(f"### 👋 {st.session_state.user}")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports"],
        icons=["bar-chart","people","cash","bank","gift","wallet","graph-up"]
    )

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    col_total = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    don_total = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    exp_total = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    st.title("📊 Dashboard")

    c1,c2,c3 = st.columns(3)
    c1.metric("Collections", col_total)
    c2.metric("Donations", don_total)
    c3.metric("Expenses", exp_total)

    st.metric("Balance", col_total + don_total - exp_total)

# =====================================
# CUSTOMERS
# =====================================
elif menu == "Customers":

    st.title("Customers")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add"):
        c.execute("INSERT INTO customers VALUES (?,?)",(name,mobile))
        conn.commit()
        st.success("Added")

    df = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df)

# =====================================
# COLLECTIONS
# =====================================
elif menu == "Collections":

    st.title("Collections")

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if len(customers)==0:
        st.warning("Add customers first")

    else:
        cust = st.selectbox("Customer", customers["name"])
        month = st.text_input("Month", datetime.datetime.now().strftime("%B %Y"))
        date = st.date_input("Start Date")
        amount = st.number_input("Amount", 0.0)

        if st.button("Save"):
            mobile = customers[customers["name"]==cust]["mobile"].values[0]
            c.execute("INSERT INTO collections VALUES (?,?,?,?,?)",(cust,mobile,month,str(date),amount))
            conn.commit()
            st.success("Saved")

    df = pd.read_sql("SELECT * FROM collections", conn)
    st.dataframe(df)

# =====================================
# LOANS
# =====================================
elif menu == "Loans":

    st.title("Loans")

    customers = pd.read_sql("SELECT * FROM customers", conn)

    cust = st.selectbox("Customer", customers["name"])
    date = st.date_input("Loan Date")
    amount = st.number_input("Amount",0.0)

    if st.button("Save Loan"):
        mobile = customers[customers["name"]==cust]["mobile"].values[0]
        c.execute("INSERT INTO loans VALUES (?,?,?,?)",(cust,mobile,str(date),amount))
        conn.commit()
        st.success("Saved")

    df = pd.read_sql("SELECT * FROM loans", conn)
    st.dataframe(df)

# =====================================
# DONATIONS
# =====================================
elif menu == "Donations":

    st.title("Donations")

    name = st.text_input("Donor")
    amount = st.number_input("Amount",0.0)

    if st.button("Save"):
        c.execute("INSERT INTO donations VALUES (?,?)",(name,amount))
        conn.commit()
        st.success("Saved")

    df = pd.read_sql("SELECT * FROM donations", conn)
    st.dataframe(df)

# =====================================
# EXPENSES
# =====================================
elif menu == "Expenses":

    st.title("Expenses")

    typ = st.text_input("Type")
    amount = st.number_input("Amount",0.0)

    if st.button("Save"):
        c.execute("INSERT INTO expenses VALUES (?,?)",(typ,amount))
        conn.commit()
        st.success("Saved")

    df = pd.read_sql("SELECT * FROM expenses", conn)
    st.dataframe(df)

# =====================================
# REPORTS
# =====================================
elif menu == "Reports":

    st.title("Reports")

    df = pd.read_sql("SELECT * FROM collections", conn)

    if not df.empty:

        month = st.selectbox("Filter Month", ["All"] + list(df["month"].unique()))

        if month != "All":
            df = df[df["month"]==month]

        st.dataframe(df)

        # Export
        csv = df.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "report.csv")

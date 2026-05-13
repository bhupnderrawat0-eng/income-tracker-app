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

c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS customers (name TEXT, mobile TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS collections (name TEXT, mobile TEXT, month TEXT, date TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS loans (name TEXT, mobile TEXT, date TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS donations (name TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS expenses (type TEXT, amount REAL)")
conn.commit()

# AUTO ADMIN
if len(c.execute("SELECT * FROM users").fetchall()) == 0:
    pwd = hashlib.sha256("admin123".encode()).hexdigest()
    c.execute("INSERT INTO users VALUES (?,?,?)", ("admin", pwd, "Admin"))
    conn.commit()

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(page_title="Bal Yuva Mangal Dal", layout="wide")

# =====================================
# PREMIUM CSS (ULTIMATE)
# =====================================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background: linear-gradient(135deg,#0f172a,#020617);
}

h1,h2,h3,h4,p,label{
    color:white !important;
}

/* HEADER CARD */
.header-box{
    background: linear-gradient(135deg,#1e293b,#0f172a);
    padding:25px;
    border-radius:20px;
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.1);
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#111827,#020617);
}

/* LOGO */
.logo{
    font-size:50px;
    text-align:center;
}

/* BUTTON */
.stButton>button{
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# LOGIN
# =====================================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("<h1 style='text-align:center;'>🔐 Login</h1>", unsafe_allow_html=True)

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

    st.markdown("""
    <div style='text-align:center'>
        <div class='logo'>🚀</div>
        <h3>Bal Yuva</h3>
        <h3 style='color:#38bdf8'>Mangal Dal</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"👤 {st.session_state.user}")
    st.markdown(f"Role: {st.session_state.role}")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users"],
        icons=["bar-chart","people","cash","bank","gift","wallet","graph-up","person"]
    )

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

# =====================================
# HEADER UI (🔥 FRONT LOGO BACK)
# =====================================
st.markdown("""
<div class='header-box'>
<h1>🚀 Bal Yuva Mangal Dal</h1>
<p>Smart Finance Management System</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    col_total = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    don_total = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    exp_total = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    c1,c2,c3 = st.columns(3)
    c1.metric("Collections", f"₹ {col_total}")
    c2.metric("Donations", f"₹ {don_total}")
    c3.metric("Expenses", f"₹ {exp_total}")

    st.metric("Balance", f"₹ {col_total + don_total - exp_total}")

# बाकी sections same (Customers, Collections, Loans, Donations, Expenses, Reports, Users)

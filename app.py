import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime

st.set_page_config(layout="wide")

# ===== CSS FIX =====
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}

.block-container{
    padding-top:0rem !important;
}

.stApp{
    background:linear-gradient(135deg,#0f172a,#020617);
}

h1,h2,h3,label{color:white !important;}

.stTextInput input, .stNumberInput input, .stSelectbox div{
    background:#111827 !important;
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ===== DATABASE =====
conn = sqlite3.connect("cloud.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, amount REAL, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS loans(name TEXT, amount REAL, date TEXT)")
conn.commit()

# ===== ADMIN =====
admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
if not c.execute("SELECT * FROM users WHERE username='admin'").fetchone():
    c.execute("INSERT INTO users VALUES(?,?,?)",("admin",admin_pass,"Admin"))
    conn.commit()

# ===== LOGIN =====
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:
    st.title("Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        enc = hashlib.sha256(p.encode()).hexdigest()
        res = c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,enc)).fetchone()

        if res:
            st.session_state.login=True
            st.session_state.user=u
            st.rerun()
        else:
            st.error("Wrong login")

    st.stop()

# ===== SIDEBAR =====
menu = st.sidebar.radio("Menu",[
    "Dashboard","Customers","Collections","Loans"
])

# ===== MONTH FUNCTION =====
def get_months():
    return [datetime.date(2026,i,1).strftime("%B %Y") for i in range(1,13)]

# ===== DASHBOARD =====
if menu=="Dashboard":
    st.title("Dashboard")

# ===== CUSTOMERS =====
elif menu=="Customers":

    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile")

    if st.button("Add"):
        c.execute("INSERT INTO customers VALUES(?,?)",(name,mobile))
        conn.commit()

    df = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df)

# ===== COLLECTION =====
elif menu=="Collections":

    dfc = pd.read_sql("SELECT * FROM customers", conn)

    if dfc.empty:
        st.warning("Add customers first")

    else:
        customer = st.selectbox(
            "Customer",
            dfc.to_dict("records"),
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        month = st.selectbox("Month", get_months())
        amount = st.number_input("Amount", min_value=0.0)
        date = st.date_input("Collection Date")

        if st.button("Save"):
            c.execute(
                "INSERT INTO collections VALUES(?,?,?,?)",
                (customer["name"], month, amount, str(date))
            )
            conn.commit()

    df = pd.read_sql("SELECT * FROM collections", conn)
    st.dataframe(df)

# ===== LOANS =====
elif menu=="Loans":

    dfc = pd.read_sql("SELECT * FROM customers", conn)

    if dfc.empty:
        st.warning("Add customers first")

    else:
        customer = st.selectbox(
            "Customer",
            dfc.to_dict("records"),
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        amount = st.number_input("Loan Amount", min_value=0.0)
        date = st.date_input("Loan Start Date")

        if st.button("Save Loan"):
            c.execute(
                "INSERT INTO loans VALUES(?,?,?)",
                (customer["name"], amount, str(date))
            )
            conn.commit()

    df = pd.read_sql("SELECT * FROM loans", conn)
    st.dataframe(df)

import streamlit as st
import pandas as pd
import sqlite3
import datetime

# ================= PAGE =================
st.set_page_config(
    page_title="Bal Yuva Enterprise",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS (WHITE BAR FIX FINAL) =================
st.markdown("""
<style>

/* REMOVE HEADER + WHITE BAR */
header {visibility:hidden;}
footer {visibility:hidden;}
#MainMenu {visibility:hidden;}
div[data-testid="stToolbar"] {display:none;}
div[data-testid="stDecoration"] {display:none;}

/* REMOVE TOP SPACE */
.block-container {
    padding-top: 0.5rem !important;
    margin-top: -20px !important;
}

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#111827,#020617);
}

/* TEXT */
h1,h2,h3,h4,p,label {
    color:white !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border:none;
    border-radius:10px;
    height:45px;
}

/* INPUT */
.stTextInput input, .stNumberInput input {
    background:#111827 !important;
    color:white !important;
}

/* CARD */
[data-testid="metric-container"] {
    background: rgba(30,41,59,0.8);
    border-radius:15px;
    padding:20px;
}

/* HEADER BOX */
.header-box {
    background: linear-gradient(135deg,#1e293b,#0f172a);
    padding:30px;
    border-radius:20px;
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
conn = sqlite3.connect("finance.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, date TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS loans(name TEXT, amount REAL, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL)")
conn.commit()

# ================= SIDEBAR =================
st.sidebar.markdown("## 🚀 Bal Yuva")
menu = st.sidebar.radio("Menu", [
    "Dashboard","Customers","Collections","Loans",
    "Donations","Expenses","Reports"
])

# ================= MONTH =================
def get_months():
    return [datetime.date(2026,i,1).strftime("%B %Y") for i in range(1,13)]

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.markdown("""
    <div class="header-box">
    <h1>🚀 Bal Yuva Mangal Dal</h1>
    <p>Enterprise Finance System</p>
    </div>
    """, unsafe_allow_html=True)

    col_total = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    don_total = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    exp_total = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
    cust_total = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Collections", f"₹ {col_total}")
    c2.metric("Donations", f"₹ {don_total}")
    c3.metric("Expenses", f"₹ {exp_total}")
    c4.metric("Customers", cust_total)

    st.metric("Balance", f"₹ {col_total + don_total - exp_total}")

# ================= CUSTOMERS =================
elif menu == "Customers":

    st.title("Customers")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")
    date = st.date_input("Start Date")

    if st.button("Add Customer"):
        c.execute("INSERT INTO customers VALUES(?,?,?)", (name,mobile,str(date)))
        conn.commit()
        st.success("Added")

    df = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df)

# ================= COLLECTIONS =================
elif menu == "Collections":

    st.title("Collections")

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if customers.empty:
        st.warning("Add customer first")
    else:
        cust = st.selectbox(
            "Customer",
            customers.to_dict("records"),
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        month = st.selectbox("Month", get_months())
        date = st.date_input("Date")
        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            c.execute("INSERT INTO collections VALUES(?,?,?,?)",
                      (cust["name"],month,str(date),amt))
            conn.commit()
            st.success("Saved")

    df = pd.read_sql("SELECT * FROM collections", conn)
    st.dataframe(df)

# ================= LOANS =================
elif menu == "Loans":

    st.title("Loans")

    name = st.text_input("Name")
    amt = st.number_input("Amount", min_value=0.0)
    date = st.date_input("Start Date")

    if st.button("Add Loan"):
        c.execute("INSERT INTO loans VALUES(?,?,?)",(name,amt,str(date)))
        conn.commit()

    df = pd.read_sql("SELECT * FROM loans", conn)
    st.dataframe(df)

# ================= DONATIONS =================
elif menu == "Donations":

    st.title("Donations")

    name = st.text_input("Donor")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        c.execute("INSERT INTO donations VALUES(?,?)",(name,amt))
        conn.commit()

    df = pd.read_sql("SELECT * FROM donations", conn)
    st.dataframe(df)

# ================= EXPENSES =================
elif menu == "Expenses":

    st.title("Expenses")

    typ = st.text_input("Type")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        c.execute("INSERT INTO expenses VALUES(?,?)",(typ,amt))
        conn.commit()

    df = pd.read_sql("SELECT * FROM expenses", conn)
    st.dataframe(df)

# ================= REPORTS =================
elif menu == "Reports":

    st.title("Reports")

    data = pd.DataFrame({
        "Type":["Collections","Donations","Expenses"],
        "Amount":[
            c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
        ]
    })

    st.dataframe(data)
    st.bar_chart(data.set_index("Type"))

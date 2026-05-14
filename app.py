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
    c.execute("CREATE TABLE IF NOT EXISTS loans(name TEXT, date TEXT, amount REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
    conn.commit()

create_tables()

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# default admin
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users VALUES (?,?,?)", ("admin", hash_pass("admin123"), "Admin"))
    conn.commit()

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva SaaS", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#020617,#0f172a);}
header, footer {visibility:hidden;}

.block-container {padding-top:1rem;}

h1,h2,h3,h4,h5,p,label {color:white !important;}

section[data-testid="stSidebar"] {background:#020617;}

.stTextInput input, .stNumberInput input, .stSelectbox div {
    background:#111827 !important;
    color:white !important;
}

.stButton>button {
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
}

/* HEADER */
.header {
    background: rgba(30,41,59,0.6);
    padding:20px;
    border-radius:20px;
    margin-bottom:25px;
}

/* SECTION BOX */
.box {
    background: rgba(30,41,59,0.6);
    padding:20px;
    border-radius:15px;
    margin-top:15px;
}

/* ✅ MOBILE SCROLL FIX */
html, body, .stApp {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)
# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):

        if not u or not p:
            st.warning("Enter username & password")
            st.stop()

        user = c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hash_pass(p))).fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user[0]
            st.session_state.role = user[2]
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()
# ================= TOP MENU (MOBILE FRIENDLY) =================
st.markdown("### 🚀 Bal Yuva SaaS")

menu = st.radio(
    "Navigation",
    ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"],
    horizontal=True
)

col_user, col_logout = st.columns([3,1])

with col_user:
    st.write(f"👤 {st.session_state.current_user}")

with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("---")

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

    st.dataframe(pd.read_sql("SELECT * FROM customers", conn))

# ================= COLLECTION =================
elif menu == "Collections":

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:

        cust = st.selectbox("Customer", customers["name"])

        month = st.selectbox("Month",
            [datetime.date(2026,m,1).strftime("%B %Y") for m in range(1,13)]
        )

        start_date = st.date_input("Start Date")
        payment_date = st.date_input("Payment Date")
        amt = st.number_input("Amount")

        if st.button("Save Collection"):
            c.execute("INSERT INTO collections VALUES (?,?,?,?,?)",
                      (cust,month,
                       start_date.strftime("%Y-%m-%d"),
                       payment_date.strftime("%Y-%m-%d"),
                       amt))
            conn.commit()

    df = pd.read_sql("SELECT * FROM collections", conn)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")

    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"]).dt.strftime("%d-%m-%Y")

    st.dataframe(df)

# ================= LOANS =================
elif menu == "Loans":

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:

        cust = st.selectbox("Customer", customers["name"])
        date = st.date_input("Loan Start Date")
        amt = st.number_input("Amount")

        if st.button("Add Loan"):
            c.execute("INSERT INTO loans VALUES (?,?,?)",
                      (cust,date.strftime("%Y-%m-%d"),amt))
            conn.commit()

    df = pd.read_sql("SELECT * FROM loans", conn)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")
    st.dataframe(df)

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

    st.subheader("📊 Summary")

    col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0
    don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    df_summary = pd.DataFrame({
        "Category": ["Collections","Loans","Donations","Expenses"],
        "Amount": [col, loan, don, exp]
    })

    st.bar_chart(df_summary.set_index("Category"))

    df = pd.read_sql("SELECT * FROM collections", conn)

    if not df.empty:

        month_filter = st.selectbox("Select Month", sorted(df["month"].unique()))
        df_month = df[df["month"] == month_filter]

        st.metric("Monthly Collection", f"₹ {df_month['amount'].sum()}")

        st.bar_chart(df_month.set_index("date")["amount"])

        cust_filter = st.selectbox("Select Customer", df_month["name"].unique())
        st.dataframe(df_month[df_month["name"] == cust_filter])

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

# ================= AI =================
elif menu == "AI":
    st.subheader("🤖 AI Insights (Coming Soon)")
    st.info("Future AI features yaha add honge")

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

    # UPDATED
    c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL, date TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
    conn.commit()

create_tables()

# SAFE column add
def safe_add_column(table, column):
    try:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")
    except:
        pass

safe_add_column("donations", "date")
safe_add_column("expenses", "date")

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

/* MOBILE FIX */
html, body, .stApp {
    overflow-y:auto !important;
    overflow-x:hidden !important;
    height:auto !important;
}

/* mobile scroll menu */
.stRadio > div {
    flex-direction: row;
    overflow-x: auto;
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

# ================= DEVICE DETECTION (FINAL FIX) =================
user_agent = st.context.headers.get("user-agent", "").lower()

if "android" in user_agent or "iphone" in user_agent:
    is_mobile = True
else:
    is_mobile = False

# ================= MENU =================
if not is_mobile:
    with st.sidebar:
        st.markdown("## 🚀 Bal Yuva SaaS")

        menu = option_menu(
            None,
            ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"],
            icons=["house","people","cash","bank","gift","credit-card","bar-chart","person","robot"],
            default_index=0,
        )
else:
    st.markdown("### 🚀 Bal Yuva SaaS")

    menu = st.radio(
        "Navigation",
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"],
        horizontal=True
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

    st.dataframe(pd.read_sql("SELECT * FROM collections", conn))

# ================= DONATIONS =================
elif menu == "Donations":

    donor = st.text_input("Donor Name")
    date = st.date_input("Date")
    amt = st.number_input("Amount")

    if st.button("Save Donation"):
        c.execute("INSERT INTO donations VALUES (?,?,?)",
                  (donor, amt, date.strftime("%Y-%m-%d")))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM donations", conn))

# ================= EXPENSES =================
elif menu == "Expenses":

    exp = st.text_input("Expense Type")
    date = st.date_input("Date")
    amt = st.number_input("Amount")

    if st.button("Save Expense"):
        c.execute("INSERT INTO expenses VALUES (?,?,?)",
                  (exp, amt, date.strftime("%Y-%m-%d")))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM expenses", conn))
# ================= REPORT =================
elif menu == "Reports":

    st.subheader("📊 Advanced Reports")

    # ================= MONTH FILTER =================
    df = pd.read_sql("SELECT * FROM collections", conn)

    if not df.empty:

        month_list = sorted(df["month"].unique())
        selected_month = st.selectbox("Select Month", month_list)

        df_month = df[df["month"] == selected_month]

        # ================= SUMMARY =================
        st.markdown("### 📅 Monthly Summary")

        total_collection = df_month["amount"].sum()

        total_expense = pd.read_sql("SELECT * FROM expenses", conn)
        total_expense = total_expense["amount"].sum() if not total_expense.empty else 0

        total_donation = pd.read_sql("SELECT * FROM donations", conn)
        total_donation = total_donation["amount"].sum() if not total_donation.empty else 0

        balance = total_collection + total_donation - total_expense

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Collection", f"₹ {total_collection}")
        c2.metric("Donations", f"₹ {total_donation}")
        c3.metric("Expenses", f"₹ {total_expense}")
        c4.metric("Balance", f"₹ {balance}")

        # ================= CHART =================
        st.markdown("### 📊 Collection Chart")

        chart_df = df_month.copy()
        chart_df["date"] = pd.to_datetime(chart_df["date"])

        st.bar_chart(chart_df.set_index("date")["amount"])

        # ================= CUSTOMER REPORT =================
        st.markdown("### 👤 Customer-wise Report")

        customer_summary = df_month.groupby("name")["amount"].sum().reset_index()

        st.dataframe(customer_summary)

        # ================= TOP CONTRIBUTORS =================
        st.markdown("### 🏆 Top Contributors")

        top_users = customer_summary.sort_values(by="amount", ascending=False).head(5)

        st.dataframe(top_users)

    else:
        st.info("No collection data available yet")
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

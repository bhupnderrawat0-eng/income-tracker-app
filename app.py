import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Bal Yuva Enterprise", layout="wide")

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
}

header, footer {visibility:hidden;}

.block-container {padding-top:1rem;}

h1,h2,h3,h4,h5,h6,p,label {
    color:white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* INPUT */
.stTextInput input, .stNumberInput input, .stSelectbox div {
    background:#111827 !important;
    color:white !important;
}

/* BUTTON */
.stButton>button {
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
}

/* HEADER CARD */
.header-box {
    background: linear-gradient(135deg, rgba(30,41,59,0.7), rgba(15,23,42,0.7));
    padding:25px;
    border-radius:20px;
    margin-bottom:20px;
    display:flex;
    align-items:center;
    gap:15px;
}

.logo {
    font-size:50px;
}

.title {
    font-size:32px;
    font-weight:800;
}

.subtitle {
    color:#94a3b8;
    font-size:14px;
}

/* METRIC CARD SPACING */
[data-testid="metric-container"] {
    background: rgba(30,41,59,0.7);
    padding:15px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION INIT
# =========================
for key in ["customers","collections","loans","donations","expenses"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "users" not in st.session_state:
    st.session_state.users = [{
        "username":"admin",
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role":"Admin"
    }]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN
# =========================
if not st.session_state.logged_in:

    st.markdown("## 🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hashlib.sha256(p.encode()).hexdigest()

        for user in st.session_state.users:
            if user["username"] == u and user["password"] == hashed:
                st.session_state.logged_in = True
                st.session_state.current_user = u
                st.session_state.role = user["role"]
                st.rerun()

        st.error("Invalid Login")

    st.stop()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🚀 Bal Yuva")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"],
        icons=["bar-chart","people","cash","bank","gift","wallet","graph-up","person","cpu"]
    )

    st.write("---")
    st.write(f"👤 {st.session_state.current_user}")
    st.write(f"Role: {st.session_state.role}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# =========================
# HEADER (LOGO FIXED HERE)
# =========================
st.markdown("""
<div class="header-box">
    <div class="logo">🚀</div>
    <div>
        <div class="title">Bal Yuva Mangal Dal</div>
        <div class="subtitle">Enterprise Finance SaaS System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    col1,col2,col3,col4 = st.columns(4)

    total_col = sum(x["amount"] for x in st.session_state.collections)
    total_loan = sum(x["amount"] for x in st.session_state.loans)
    total_don = sum(x["amount"] for x in st.session_state.donations)
    total_exp = sum(x["amount"] for x in st.session_state.expenses)

    col1.metric("Collections", f"₹ {total_col}")
    col2.metric("Loans", f"₹ {total_loan}")
    col3.metric("Donations", f"₹ {total_don}")
    col4.metric("Expenses", f"₹ {total_exp}")

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# =========================
# बाकी modules same
# =========================
elif menu == "Customers":
    st.title("Customers")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add"):
        st.session_state.customers.append({"name":name,"mobile":mobile})

    st.dataframe(pd.DataFrame(st.session_state.customers))

elif menu == "Collections":
    st.title("Collections")

    if st.session_state.customers:
        cust = st.selectbox("Customer", st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})")

        month = st.selectbox("Month",
            [datetime.date(2026,m,1).strftime("%B %Y") for m in range(1,13)]
        )

        date = st.date_input("Start Date")
        amt = st.number_input("Amount")

        if st.button("Save"):
            st.session_state.collections.append({
                "name":cust["name"],
                "month":month,
                "date":str(date),
                "amount":amt
            })

    st.dataframe(pd.DataFrame(st.session_state.collections))

elif menu == "Loans":
    st.title("Loans")

    if st.session_state.customers:
        cust = st.selectbox("Customer", st.session_state.customers,
            format_func=lambda x: x["name"])

        date = st.date_input("Loan Start Date")
        amt = st.number_input("Amount")

        if st.button("Add Loan"):
            st.session_state.loans.append({
                "name":cust["name"],
                "date":str(date),
                "amount":amt
            })

    st.dataframe(pd.DataFrame(st.session_state.loans))

elif menu == "Reports":
    df = pd.DataFrame({
        "Category":["Collections","Loans","Donations","Expenses"],
        "Amount":[
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.loans),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })
    st.bar_chart(df.set_index("Category"))

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bal Yuva Finance Pro Max",
    page_icon="🚀",
    layout="wide"
)

# =========================
# DARK PREMIUM CSS (FIX WHITE ISSUE)
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
}
header, footer {visibility:hidden;}
.block-container {padding-top:1rem;}

section[data-testid="stSidebar"] {
    background:#020617;
}

h1,h2,h3,h4,h5,h6,p,label,span {
    color:white !important;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    background:#111827 !important;
    color:white !important;
}

.stButton>button {
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
for key in ["customers","collections","loans","donations","expenses"]:
    if key not in st.session_state:
        st.session_state[key] = []

# LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

# =========================
# SIDEBAR MENU
# =========================
with st.sidebar:
    st.markdown("## 🚀 Bal Yuva Finance")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports"],
        icons=["bar-chart","people","cash","bank","gift","wallet","graph-up"]
    )

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.markdown("## 📊 Dashboard")

    col1,col2,col3,col4 = st.columns(4)

    total_col = sum(x["amount"] for x in st.session_state.collections)
    total_loan = sum(x["amount"] for x in st.session_state.loans)
    total_don = sum(x["amount"] for x in st.session_state.donations)
    total_exp = sum(x["amount"] for x in st.session_state.expenses)

    with col1:
        st.metric("Collections", f"₹ {total_col}")
    with col2:
        st.metric("Loans", f"₹ {total_loan}")
    with col3:
        st.metric("Donations", f"₹ {total_don}")
    with col4:
        st.metric("Expenses", f"₹ {total_exp}")

    st.metric("Net Balance", f"₹ {total_col + total_don - total_exp}")

# =========================
# CUSTOMERS
# =========================
elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        st.session_state.customers.append({
            "name": name,
            "mobile": mobile
        })

    if st.session_state.customers:
        st.dataframe(pd.DataFrame(st.session_state.customers))

# =========================
# COLLECTIONS
# =========================
elif menu == "Collections":

    st.title("💰 Collections")

    if not st.session_state.customers:
        st.warning("Add customer first")
    else:
        cust = st.selectbox("Customer", st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})")

        month = st.selectbox("Month",
            [datetime.date(2026, m, 1).strftime("%B %Y") for m in range(1,13)]
        )

        date = st.date_input("Collection Date")
        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            st.session_state.collections.append({
                "name": cust["name"],
                "month": month,
                "date": str(date),
                "amount": amt
            })

    if st.session_state.collections:
        st.dataframe(pd.DataFrame(st.session_state.collections))

# =========================
# LOANS
# =========================
elif menu == "Loans":

    st.title("🏦 Loans")

    if not st.session_state.customers:
        st.warning("Add customer first")
    else:
        cust = st.selectbox("Customer", st.session_state.customers,
            format_func=lambda x: x["name"])

        start = st.date_input("Loan Start Date")
        amt = st.number_input("Loan Amount")

        if st.button("Add Loan"):
            st.session_state.loans.append({
                "name": cust["name"],
                "start": str(start),
                "amount": amt
            })

    if st.session_state.loans:
        st.dataframe(pd.DataFrame(st.session_state.loans))

# =========================
# DONATIONS
# =========================
elif menu == "Donations":

    st.title("🎁 Donations")

    donor = st.text_input("Donor Name")
    amt = st.number_input("Amount")

    if st.button("Add Donation"):
        st.session_state.donations.append({
            "donor": donor,
            "amount": amt
        })

    if st.session_state.donations:
        st.dataframe(pd.DataFrame(st.session_state.donations))

# =========================
# EXPENSES
# =========================
elif menu == "Expenses":

    st.title("💸 Expenses")

    etype = st.text_input("Expense Type")
    amt = st.number_input("Amount")

    if st.button("Add Expense"):
        st.session_state.expenses.append({
            "type": etype,
            "amount": amt
        })

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses))

# =========================
# REPORTS
# =========================
elif menu == "Reports":

    st.title("📊 Reports")

    df = pd.DataFrame({
        "Category":["Collections","Loans","Donations","Expenses"],
        "Amount":[
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.loans),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.dataframe(df)
    st.bar_chart(df.set_index("Category"))

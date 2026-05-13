import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Bal Yuva Mangal Dal", layout="wide")

# ===============================
# SIMPLE DARK UI
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
}
h1,h2,h3,h4,h5,h6,p,label {
    color:white !important;
}
section[data-testid="stSidebar"]{
    background:#111827;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    st.session_state.users = [
        {"name":"admin","password":hashlib.sha256("admin123".encode()).hexdigest(),"role":"Admin"}
    ]

if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "loans" not in st.session_state:
    st.session_state.loans = []

# ===============================
# LOGIN
# ===============================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        hashed = hashlib.sha256(pwd.encode()).hexdigest()

        for u in st.session_state.users:
            if u["name"] == user and u["password"] == hashed:
                st.session_state.logged_in = True
                st.session_state.current_user = u["name"]
                st.session_state.current_role = u["role"]
                st.rerun()

        st.error("Wrong credentials")

    st.stop()

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:

    st.markdown("## 🚀 Bal Yuva Mangal Dal")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users"],
        icons=["house","people","cash","bank","gift","wallet","bar-chart","person"],
        default_index=0
    )

# ===============================
# DASHBOARD
# ===============================
if menu == "Dashboard":

    st.title("📊 Dashboard")

    total_c = sum(x["amount"] for x in st.session_state.collections)
    total_d = sum(x["amount"] for x in st.session_state.donations)
    total_e = sum(x["amount"] for x in st.session_state.expenses)

    balance = total_c + total_d - total_e

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_c}")
    c2.metric("Donations", f"₹ {total_d}")
    c3.metric("Expenses", f"₹ {total_e}")
    c4.metric("Customers", len(st.session_state.customers))

    st.metric("Net Balance", f"₹ {balance}")

# ===============================
# CUSTOMERS
# ===============================
elif menu == "Customers":

    st.title("👥 Customers")

    col1,col2,col3 = st.columns(3)

    with col1:
        name = st.text_input("Name")

    with col2:
        mobile = st.text_input("Mobile")

    with col3:
        date = st.date_input("Meeting Date")

    if st.button("Add Customer"):

        if name and mobile:
            st.session_state.customers.append({
                "name":name,
                "mobile":mobile,
                "meeting_date":str(date)
            })
            st.success("Added")
        else:
            st.error("Fill all fields")

    if st.session_state.customers:
        st.dataframe(pd.DataFrame(st.session_state.customers))

# ===============================
# COLLECTIONS
# ===============================
elif menu == "Collections":

    st.title("💵 Collections")

    if not st.session_state.customers:
        st.warning("Add customers first")

    else:
        customer = st.selectbox(
            "Customer",
            st.session_state.customers,
            format_func=lambda x:f"{x['name']} ({x['mobile']})"
        )

        month = st.selectbox(
            "Month",
            [datetime.datetime.now().strftime("%B %Y")] + [
                "January 2026","February 2026","March 2026",
                "April 2026","May 2026","June 2026",
                "July 2026","August 2026","September 2026",
                "October 2026","November 2026","December 2026"
            ]
        )

        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Save Collection"):
            st.session_state.collections.append({
                "name":customer["name"],
                "mobile":customer["mobile"],
                "month":month,
                "amount":amount
            })
            st.success("Saved")

    if st.session_state.collections:

        df = pd.DataFrame(st.session_state.collections)

        m = st.selectbox("Filter Month", ["All"] + list(df["month"].unique()))

        if m != "All":
            df = df[df["month"] == m]

        st.dataframe(df)

# ===============================
# LOANS
# ===============================
elif menu == "Loans":

    st.title("🏦 Loans")

    col1,col2,col3 = st.columns(3)

    with col1:
        name = st.text_input("Borrower")

    with col2:
        amount = st.number_input("Amount", min_value=0.0)

    with col3:
        interest = st.number_input("Interest %", min_value=0.0)

    duration = st.number_input("Months", min_value=1)

    if st.button("Add Loan"):

        total = amount + (amount*interest*duration/100)

        st.session_state.loans.append({
            "name":name,
            "amount":amount,
            "interest":interest,
            "duration":duration,
            "total":total,
            "paid":0
        })

        st.success("Loan Added")

    if st.session_state.loans:

        df = pd.DataFrame(st.session_state.loans)
        st.dataframe(df)

        loan = st.selectbox(
            "Repay Loan",
            st.session_state.loans,
            format_func=lambda x:f"{x['name']} ₹{x['amount']}"
        )

        pay = st.number_input("Pay Amount", min_value=0.0)

        if st.button("Pay"):
            loan["paid"] += pay
            st.success("Updated")

# ===============================
# DONATIONS
# ===============================
elif menu == "Donations":

    st.title("🎁 Donations")

    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        st.session_state.donations.append({"amount":amt})
        st.success("Saved")

# ===============================
# EXPENSES
# ===============================
elif menu == "Expenses":

    st.title("💸 Expenses")

    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        st.session_state.expenses.append({"amount":amt})
        st.success("Saved")

# ===============================
# REPORTS
# ===============================
elif menu == "Reports":

    st.title("📊 Reports")

    df = pd.DataFrame({
        "Category":["Collections","Donations","Expenses"],
        "Amount":[
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.dataframe(df)
    st.bar_chart(df.set_index("Category"))

# ===============================
# USERS
# ===============================
elif menu == "Users":

    st.title("👤 Users")

    st.success(f"Logged in: {st.session_state.current_user}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

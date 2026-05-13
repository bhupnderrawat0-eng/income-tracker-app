import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Bal Yuva AI Finance", layout="wide")

# =========================
# DARK UI FIX (NO WHITE)
# =========================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f172a,#020617);}
header, footer {visibility:hidden;}
h1,h2,h3,h4,h5,h6,p,label,span {color:white !important;}

.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    background:#111827 !important;
    color:white !important;
}

.stButton>button {
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
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
# LOGIN SYSTEM
# =========================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        hashed = hashlib.sha256(pwd.encode()).hexdigest()

        for u in st.session_state.users:
            if u["username"] == user and u["password"] == hashed:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.session_state.role = u["role"]
                st.rerun()

        st.error("Wrong credentials")

    st.stop()

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.markdown("## 🚀 Bal Yuva AI")

    menu = option_menu(None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI Insights"],
        icons=["bar-chart","people","cash","bank","gift","wallet","graph-up","person","robot"]
    )

    st.write("---")
    st.write(f"👤 {st.session_state.current_user}")
    st.write(f"Role: {st.session_state.role}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("📊 Dashboard")

    total_col = sum(x["amount"] for x in st.session_state.collections)
    total_loan = sum(x["amount"] for x in st.session_state.loans)
    total_don = sum(x["amount"] for x in st.session_state.donations)
    total_exp = sum(x["amount"] for x in st.session_state.expenses)

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Collections", f"₹ {total_col}")
    col2.metric("Loans", f"₹ {total_loan}")
    col3.metric("Donations", f"₹ {total_don}")
    col4.metric("Expenses", f"₹ {total_exp}")

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# =========================
# CUSTOMERS
# =========================
elif menu == "Customers":

    st.title("Customers")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add"):
        st.session_state.customers.append({"name":name,"mobile":mobile})

    if st.session_state.customers:
        st.dataframe(pd.DataFrame(st.session_state.customers))

# =========================
# COLLECTIONS
# =========================
elif menu == "Collections":

    st.title("Collections")

    if not st.session_state.customers:
        st.warning("Add customer first")
    else:
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

    if st.session_state.collections:
        st.dataframe(pd.DataFrame(st.session_state.collections))

# =========================
# LOANS
# =========================
elif menu == "Loans":

    st.title("Loans")

    if not st.session_state.customers:
        st.warning("Add customer first")
    else:
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

    if st.session_state.loans:
        st.dataframe(pd.DataFrame(st.session_state.loans))

# =========================
# DONATIONS
# =========================
elif menu == "Donations":

    st.title("Donations")

    donor = st.text_input("Donor Name")
    amt = st.number_input("Amount")

    if st.button("Add Donation"):
        st.session_state.donations.append({
            "donor":donor,
            "amount":amt
        })

    if st.session_state.donations:
        st.dataframe(pd.DataFrame(st.session_state.donations))

# =========================
# EXPENSES
# =========================
elif menu == "Expenses":

    st.title("Expenses")

    etype = st.text_input("Expense Type")
    amt = st.number_input("Amount")

    if st.button("Add Expense"):
        st.session_state.expenses.append({
            "type":etype,
            "amount":amt
        })

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses))

# =========================
# REPORTS
# =========================
elif menu == "Reports":

    st.title("Reports")

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

# =========================
# USERS
# =========================
elif menu == "Users":

    st.title("Users")

    if st.session_state.role != "Admin":
        st.warning("Admin only")
    else:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        r = st.selectbox("Role",["Admin","Editor","Viewer"])

        if st.button("Add User"):
            st.session_state.users.append({
                "username":u,
                "password":hashlib.sha256(p.encode()).hexdigest(),
                "role":r
            })
            st.success("Added")

    st.dataframe(pd.DataFrame(st.session_state.users))

# =========================
# AI INSIGHTS
# =========================
elif menu == "AI Insights":

    st.title("AI Insights")

    col = sum(x["amount"] for x in st.session_state.collections)
    exp = sum(x["amount"] for x in st.session_state.expenses)

    balance = col - exp

    st.metric("Balance", f"₹ {balance}")

    if balance > 0:
        st.success("Profit")
    elif balance < 0:
        st.error("Loss")
    else:
        st.info("Neutral")

    if exp > col:
        st.warning("Reduce expenses")
    else:
        st.info("Good control")

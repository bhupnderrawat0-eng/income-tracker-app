import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Bal Yuva Mangal Dal",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# PASSWORD HASH
# =====================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================================
# SESSION STATE INIT
# =====================================================

if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "users" not in st.session_state:
    st.session_state.users = [
        {
            "name": "admin",
            "password": hash_password("admin123"),
            "role": "Admin"
        }
    ]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_role" not in st.session_state:
    st.session_state.current_role = ""

# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        for user in st.session_state.users:

            if (
                user["name"] == username and
                user["password"] == hash_password(password)
            ):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.current_role = user["role"]
                st.rerun()

        st.error("Invalid Username or Password")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🚀 Bal Yuva Mangal Dal")

    st.write(f"👤 {st.session_state.current_user}")
    st.write(f"🔑 Role: {st.session_state.current_role}")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.current_role = ""
        st.rerun()

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Donations","Expenses","Reports","Users"],
        icons=["grid","people","cash","gift","wallet","bar-chart","person"],
        default_index=0
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    collections_total = sum(x["amount"] for x in st.session_state.collections)
    donations_total = sum(x["amount"] for x in st.session_state.donations)
    expenses_total = sum(x["amount"] for x in st.session_state.expenses)

    balance = collections_total + donations_total - expenses_total

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Collections", f"₹ {collections_total}")
    c2.metric("Donations", f"₹ {donations_total}")
    c3.metric("Expenses", f"₹ {expenses_total}")
    c4.metric("Customers", len(st.session_state.customers))

    st.metric("Net Balance", f"₹ {balance}")

# =====================================================
# CUSTOMERS
# =====================================================

elif menu == "Customers":

    st.title("Customers")

    name = st.text_input("Customer Name")

    if st.button("Add Customer"):

        if name:
            st.session_state.customers.append(name)
            st.success("Added")

    st.dataframe(pd.DataFrame(st.session_state.customers, columns=["Name"]))

# =====================================================
# COLLECTIONS
# =====================================================

elif menu == "Collections":

    st.title("Collections")

    if not st.session_state.customers:
        st.warning("Add customers first")

    else:
        customer = st.selectbox("Customer", st.session_state.customers)
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            st.session_state.collections.append({
                "customer": customer,
                "amount": amount
            })
            st.success("Saved")

# =====================================================
# DONATIONS
# =====================================================

elif menu == "Donations":

    st.title("Donations")

    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        st.session_state.donations.append({"amount": amount})
        st.success("Saved")

# =====================================================
# EXPENSES
# =====================================================

elif menu == "Expenses":

    st.title("Expenses")

    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        st.session_state.expenses.append({"amount": amount})
        st.success("Saved")

# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":

    st.title("Reports")

    df = pd.DataFrame({
        "Category": ["Collections","Donations","Expenses"],
        "Amount": [
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.dataframe(df)
    st.bar_chart(df.set_index("Category"))

# =====================================================
# USERS
# =====================================================

elif menu == "Users":

    st.title("User Management")

    if st.session_state.current_role != "Admin":
        st.warning("Only Admin can manage users")
    else:

        st.subheader("Add User")

        col1,col2,col3 = st.columns(3)

        with col1:
            username = st.text_input("Username")

        with col2:
            password = st.text_input("Password", type="password")

        with col3:
            role = st.selectbox("Role", ["Admin","Editor","Viewer"])

        if st.button("Add User"):

            if username and password:

                exists = any(u["name"] == username for u in st.session_state.users)

                if exists:
                    st.error("User exists")
                else:
                    st.session_state.users.append({
                        "name": username,
                        "password": hash_password(password),
                        "role": role
                    })
                    st.success("User added")
                    st.rerun()

        st.subheader("All Users")

        st.dataframe(pd.DataFrame(st.session_state.users))

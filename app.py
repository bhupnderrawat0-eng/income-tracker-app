import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_option_menu import option_menu

from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Finance Tracker Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.stApp {
    background: #0e1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

div[data-testid="metric-container"] {
    background: linear-gradient(135deg,#1f2937,#111827);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #374151;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.4);
}

div[data-testid="metric-container"] label {
    color: #9ca3af !important;
}

div[data-testid="metric-container"] div {
    color: white !important;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(90deg,#2563eb,#1d4ed8);
    color: white;
    border: none;
    font-weight: bold;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.stNumberInput>div>div>input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {
            "password": "admin123",
            "role": "admin",
            "active": True
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "loans" not in st.session_state:
    st.session_state.loans = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# =====================================================
# LOGIN FUNCTION
# =====================================================

def login(username, password):

    users = st.session_state.users

    if username in users:

        if (
            users[username]["password"] == password
            and users[username]["active"]
        ):

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]

            return True

    return False

# =====================================================
# LOGIN SCREEN
# =====================================================

if not st.session_state.logged_in:

    st.title("🔐 Smart Finance Tracker Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        success = login(username, password)

        if success:
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Login")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=100
    )

    st.markdown("## 💰 Smart Finance Tracker")

    menu = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Customers",
            "Collections",
            "Loans",
            "Donations",
            "Expenses",
            "Reports",
            "Users"
        ],
        icons=[
            "house",
            "people",
            "cash-stack",
            "bank",
            "gift",
            "wallet2",
            "bar-chart",
            "person"
        ],
        default_index=0,
    )

    st.divider()

    st.write(f"👤 {st.session_state.username}")
    st.write(f"🔐 {st.session_state.role}")

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.title("📊 Finance Dashboard")

    collections_total = sum(
        x["amount"]
        for x in st.session_state.collections
    )

    donations_total = sum(
        x["amount"]
        for x in st.session_state.donations
    )

    expenses_total = sum(
        x["amount"]
        for x in st.session_state.expenses
    )

    total_loans = sum(
        x["loan_amount"]
        for x in st.session_state.loans
    )

    returned_loans = sum(
        x["returned"]
        for x in st.session_state.loans
    )

    remaining_loans = total_loans - returned_loans

    balance = (
        collections_total
        + donations_total
        - expenses_total
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💵 Collections", f"₹ {collections_total:,.0f}")
    c2.metric("🎁 Donations", f"₹ {donations_total:,.0f}")
    c3.metric("💸 Expenses", f"₹ {expenses_total:,.0f}")
    c4.metric("🏦 Loan Pending", f"₹ {remaining_loans:,.0f}")

    st.divider()

    c5, c6 = st.columns(2)

    c5.metric("🪙 Net Balance", f"₹ {balance:,.0f}")
    c6.metric("👥 Customers", len(st.session_state.customers))

    st.divider()

    chart_data = pd.DataFrame({
        "Category": [
            "Collections",
            "Donations",
            "Expenses"
        ],
        "Amount": [
            collections_total,
            donations_total,
            expenses_total
        ]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Amount",
        text="Amount",
        title="Finance Overview"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# CUSTOMERS
# =====================================================

elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input("Customer Name")

    if st.button("Add Customer"):

        if name != "":

            st.session_state.customers.append(name)

            st.success("Customer Added")

    if st.session_state.customers:

        df = pd.DataFrame(
            st.session_state.customers,
            columns=["Customer Name"]
        )

        st.dataframe(df, use_container_width=True)

# =====================================================
# COLLECTIONS
# =====================================================

elif menu == "Collections":

    st.title("💵 Collections")

    if len(st.session_state.customers) == 0:

        st.warning("Please add customers first")

    else:

        customer = st.selectbox(
            "Customer",
            st.session_state.customers
        )

        month = st.text_input(
            "Month",
            value=datetime.now().strftime("%B %Y")
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        status = st.selectbox(
            "Status",
            ["Paid", "Pending"]
        )

        payment_date = st.date_input(
            "Payment Date"
        )

        if st.button("Save Collection"):

            st.session_state.collections.append({
                "customer": customer,
                "month": month,
                "amount": amount,
                "status": status,
                "date": str(payment_date)
            })

            st.success("Collection Saved")

# =====================================================
# LOANS
# =====================================================

elif menu == "Loans":

    st.title("🏦 Loans")

    tab1, tab2 = st.tabs([
        "Start Loan",
        "Loan Management"
    ])

    with tab1:

        if len(st.session_state.customers) == 0:

            st.warning("Please add customers first")

        else:

            customer = st.selectbox(
                "Select Customer",
                st.session_state.customers
            )

            loan_amount = st.number_input(
                "Loan Amount",
                min_value=0.0
            )

            interest_rate = st.number_input(
                "Interest %",
                min_value=0.0
            )

            if st.button("Start Loan"):

                st.session_state.loans.append({
                    "customer": customer,
                    "loan_amount": loan_amount,
                    "returned": 0.0,
                    "interest_rate": interest_rate
                })

                st.success("Loan Started")

    with tab2:

        if len(st.session_state.loans) == 0:

            st.info("No loans available")

        else:

            customer_names = [
                x["customer"]
                for x in st.session_state.loans
            ]

            selected_customer = st.selectbox(
                "Select Customer",
                customer_names
            )

            loan = next(
                x for x in st.session_state.loans
                if x["customer"] == selected_customer
            )

            original_loan = loan["loan_amount"]
            returned = loan["returned"]

            remaining = original_loan - returned

            interest = (
                remaining
                * loan["interest_rate"]
                / 100
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("🏦 Original Loan", f"₹ {original_loan}")
            c2.metric("💰 Returned", f"₹ {returned}")
            c3.metric("📄 Remaining", f"₹ {remaining}")
            c4.metric("📈 Interest", f"₹ {interest}")

            return_amount = st.number_input(
                "Return Amount",
                min_value=0.0
            )

            if st.button("Save Return"):

                loan["returned"] += return_amount

                st.success("Return Saved")

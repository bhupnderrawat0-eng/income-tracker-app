# =========================================
# SMART FINANCE TRACKER PRO
# EASY FINANCE VERSION
# =========================================

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Smart Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# =========================================
# DATABASE
# =========================================

conn = sqlite3.connect(
    "tracker.db",
    check_same_thread=False
)

c = conn.cursor()

# =========================================
# TABLES
# =========================================

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    collection_start_date TEXT,
    loan_start_date TEXT,
    monthly_collection REAL,
    loan_amount REAL,
    interest_rate REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    month TEXT,
    amount REAL,
    status TEXT,
    payment_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS interest_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS loan_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_date TEXT
)
""")

conn.commit()

# =========================================
# LOGIN
# =========================================

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == ADMIN_USER
            and
            password == ADMIN_PASS
        ):

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.stop()

# =========================================
# MONTHS
# =========================================

month_options = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Customers",
        "Collections",
        "Loans",
        "Interest",
        "Pending",
        "Reports"
    ]
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.rerun()

# =========================================
# LOAD DATA
# =========================================

customers = pd.read_sql(
    "SELECT * FROM customers",
    conn
)

collections = pd.read_sql(
    "SELECT * FROM collections",
    conn
)

interest_payments = pd.read_sql(
    "SELECT * FROM interest_payments",
    conn
)

loan_payments = pd.read_sql(
    "SELECT * FROM loan_payments",
    conn
)

# =========================================
# DASHBOARD
# =========================================

if menu == "Dashboard":

    st.title("📊 Finance Dashboard")

    total_collection = (
        collections["amount"].sum()
        if not collections.empty else 0
    )

    total_loan = (
        customers["loan_amount"].sum()
        if not customers.empty else 0
    )

    total_loan_received = (
        loan_payments["amount"].sum()
        if not loan_payments.empty else 0
    )

    total_interest_received = (
        interest_payments["amount"].sum()
        if not interest_payments.empty else 0
    )

    remaining_loan = (
        total_loan
        -
        total_loan_received
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Collection Received",
        f"₹ {total_collection}"
    )

    col2.metric(
        "🏦 Loan Given",
        f"₹ {total_loan}"
    )

    col3.metric(
        "💳 Loan Returned",
        f"₹ {total_loan_received}"
    )

    col4.metric(
        "📉 Loan Remaining",
        f"₹ {remaining_loan}"
    )

    st.divider()

    st.metric(
        "📈 Interest Received",
        f"₹ {total_interest_received}"
    )

# =========================================
# CUSTOMERS
# =========================================

elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input(
        "Customer Name"
    )

    mobile = st.text_input(
        "Mobile Number"
    )

    collection_start_date = st.date_input(
        "Collection Start Date"
    )

    loan_start_date = st.date_input(
        "Loan Start Date"
    )

    monthly_collection = st.number_input(
        "Monthly Collection Amount",
        min_value=0.0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0
    )

    interest_rate = st.number_input(
        "Monthly Interest Rate (%)",
        min_value=0.0
    )

    monthly_interest = (
        loan_amount
        *
        interest_rate
        / 100
    )

    st.info(
        f"📈 Monthly Interest = ₹ {monthly_interest}"
    )

    if st.button("Save Customer"):

        c.execute(
            """
            INSERT INTO customers
            (
                name,
                mobile,
                collection_start_date,
                loan_start_date,
                monthly_collection,
                loan_amount,
                interest_rate
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                mobile,
                str(collection_start_date),
                str(loan_start_date),
                monthly_collection,
                loan_amount,
                interest_rate
            )
        )

        conn.commit()

        st.success(
            "Customer Added"
        )

    st.divider()

    st.dataframe(
        customers.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# COLLECTIONS
# =========================================

elif menu == "Collections":

    st.title("💵 Collections")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    month = st.selectbox(
        "Select Month",
        month_options
    )

    amount = st.number_input(
        "Collection Amount",
        min_value=0.0
    )

    status = st.selectbox(
        "Status",
        [
            "Paid",
            "Pending",
            "Partial"
        ]
    )

    if st.button("Save Collection"):

        c.execute(
            """
            INSERT INTO collections
            (
                customer_name,
                month,
                amount,
                status,
                payment_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                customer_name,
                month,
                amount,
                status,
                str(date.today())
            )
        )

        conn.commit()

        st.success(
            "Collection Saved"
        )

    st.divider()

    st.dataframe(
        collections.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# LOANS
# =========================================

elif menu == "Loans":

    st.title("🏦 Loan Management")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    customer = customers[
        customers["name"]
        ==
        customer_name
    ].iloc[0]

    loan_amount = customer[
        "loan_amount"
    ]

    loan_paid = loan_payments[
        loan_payments["customer_name"]
        ==
        customer_name
    ]["amount"].sum()

    loan_remaining = (
        loan_amount
        -
        loan_paid
    )

    st.subheader("📊 Loan Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏦 Loan Given",
        f"₹ {loan_amount}"
    )

    col2.metric(
        "💳 Loan Returned",
        f"₹ {loan_paid}"
    )

    col3.metric(
        "📉 Loan Remaining",
        f"₹ {loan_remaining}"
    )

    st.divider()

    amount = st.number_input(
        "Loan Payment Received",
        min_value=0.0
    )

    if st.button("Save Loan Payment"):

        c.execute(
            """
            INSERT INTO loan_payments
            (
                customer_name,
                amount,
                payment_date
            )
            VALUES (?, ?, ?)
            """,
            (
                customer_name,
                amount,
                str(date.today())
            )
        )

        conn.commit()

        st.success(
            "Loan Payment Saved"
        )

    st.divider()

    st.dataframe(
        loan_payments.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# INTEREST
# =========================================

elif menu == "Interest":

    st.title("📈 Interest Management")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    customer = customers[
        customers["name"]
        ==
        customer_name
    ].iloc[0]

    loan_amount = customer[
        "loan_amount"
    ]

    interest_rate = customer[
        "interest_rate"
    ]

    loan_start = datetime.strptime(
        customer["loan_start_date"],
        "%Y-%m-%d"
    ).date()

    today = date.today()

    months_passed = (
        (today.year - loan_start.year)
        * 12
        +
        (today.month - loan_start.month)
    )

    monthly_interest = (
        loan_amount
        *
        interest_rate
        / 100
    )

    total_interest = (
        monthly_interest
        *
        months_passed
    )

    interest_paid = interest_payments[
        interest_payments["customer_name"]
        ==
        customer_name
    ]["amount"].sum()

    interest_remaining = (
        total_interest
        -
        interest_paid
    )

    st.subheader("📊 Interest Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📈 Monthly Interest",
        f"₹ {monthly_interest}"
    )

    col2.metric(
        "📅 Months Passed",
        months_passed
    )

    col3.metric(
        "💰 Total Interest",
        f"₹ {total_interest}"
    )

    col4.metric(
        "❌ Interest Remaining",
        f"₹ {interest_remaining}"
    )

    st.divider()

    amount = st.number_input(
        "Interest Payment Received",
        min_value=0.0
    )

    if st.button("Save Interest Payment"):

        c.execute(
            """
            INSERT INTO interest_payments
            (
                customer_name,
                amount,
                payment_date
            )
            VALUES (?, ?, ?)
            """,
            (
                customer_name,
                amount,
                str(date.today())
            )
        )

        conn.commit()

        st.success(
            "Interest Saved"
        )

    st.divider()

    st.dataframe(
        interest_payments.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# PENDING
# =========================================

elif menu == "Pending":

    st.title("❌ Pending Collections")

    selected_month = st.selectbox(
        "Select Month",
        month_options
    )

    pending_list = []

    paid_customers = collections[
        (
            collections["month"]
            ==
            selected_month
        )
        &
        (
            collections["status"]
            ==
            "Paid"
        )
    ]["customer_name"].tolist()

    for _, customer in customers.iterrows():

        collection_start = datetime.strptime(
            customer["collection_start_date"],
            "%Y-%m-%d"
        )

        start_month = (
            collection_start.month
        )

        selected_index = (
            month_options.index(
                selected_month
            )
            + 1
        )

        if selected_index >= start_month:

            if customer["name"] not in paid_customers:

                pending_list.append({

                    "Customer":
                    customer["name"],

                    "Mobile":
                    customer["mobile"],

                    "Pending Amount":
                    customer[
                        "monthly_collection"
                    ]
                })

    pending_df = pd.DataFrame(
        pending_list
    )

    st.dataframe(
        pending_df.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# REPORTS
# =========================================

elif menu == "Reports":

    st.title("📑 Reports")

    st.subheader("👥 Customers")

    st.dataframe(
        customers.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("💵 Collections")

    st.dataframe(
        collections.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("🏦 Loan Payments")

    st.dataframe(
        loan_payments.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("📈 Interest Payments")

    st.dataframe(
        interest_payments.reset_index(drop=True),
        use_container_width=True
    )

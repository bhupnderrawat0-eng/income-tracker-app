# =========================================
# SMART FINANCE TRACKER PRO
# FINAL PROFESSIONAL VERSION
# =========================================

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Smart Finance Tracker Pro",
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
# CREATE TABLES
# =========================================

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    loan_date TEXT,
    monthly_collection REAL,
    loan_amount REAL,
    interest_rate REAL,
    emi_amount REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS monthly_collections (
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
CREATE TABLE IF NOT EXISTS principal_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT,
    amount REAL,
    expense_date TEXT
)
""")

conn.commit()

# =========================================
# LOGIN SYSTEM
# =========================================

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

VIEW_USER = "viewer"
VIEW_PASS = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================
# LOGIN PAGE
# =========================================

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
            st.session_state.role = "admin"
            st.rerun()

        elif (
            username == VIEW_USER
            and
            password == VIEW_PASS
        ):

            st.session_state.logged_in = True
            st.session_state.role = "viewer"
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
        "Monthly Collections",
        "Loan Management",
        "Interest Management",
        "Pending Collections",
        "Customer Profile",
        "Expenses",
        "Reports"
    ]
)

st.sidebar.write(
    f"👤 Logged in as: {st.session_state.role}"
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
    "SELECT * FROM monthly_collections",
    conn
)

interest_payments = pd.read_sql(
    "SELECT * FROM interest_payments",
    conn
)

principal_payments = pd.read_sql(
    "SELECT * FROM principal_payments",
    conn
)

expenses = pd.read_sql(
    "SELECT * FROM expenses",
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

    total_interest_received = (
        interest_payments["amount"].sum()
        if not interest_payments.empty else 0
    )

    total_principal_received = (
        principal_payments["amount"].sum()
        if not principal_payments.empty else 0
    )

    remaining_loan = (
        total_loan
        -
        total_principal_received
    )

    total_expense = (
        expenses["amount"].sum()
        if not expenses.empty else 0
    )

    total_pending_collection = 0

    for _, customer in customers.iterrows():

        customer_name = customer["name"]

        customer_collection = customer[
            "monthly_collection"
        ]

        start_date = datetime.strptime(
            customer["loan_date"],
            "%Y-%m-%d"
        )

        start_month = start_date.month

        paid_months = []

        customer_paid_data = collections[
            (
                collections["customer_name"]
                ==
                customer_name
            )
            &
            (
                collections["status"]
                ==
                "Paid"
            )
        ]

        if not customer_paid_data.empty:

            paid_months = customer_paid_data[
                "month"
            ].tolist()

        pending_count = 0

        for i in range(start_month - 1, 12):

            month_name = month_options[i]

            if month_name not in paid_months:

                pending_count += 1

        total_pending_collection += (
            pending_count
            *
            customer_collection
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Collection Received",
        f"₹ {total_collection}"
    )

    col2.metric(
        "❌ Pending Collection",
        f"₹ {total_pending_collection}"
    )

    col3.metric(
        "🏦 Total Loan",
        f"₹ {total_loan}"
    )

    col4.metric(
        "📉 Remaining Loan",
        f"₹ {remaining_loan}"
    )

    st.divider()

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "📈 Interest Received",
        f"₹ {total_interest_received}"
    )

    col6.metric(
        "💸 Expenses",
        f"₹ {total_expense}"
    )

    col7.metric(
        "👥 Customers",
        len(customers)
    )

# =========================================
# CUSTOMERS
# =========================================

elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input("Customer Name")

    mobile = st.text_input("Mobile Number")

    loan_date = st.date_input(
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

    emi_amount = st.number_input(
        "Monthly EMI Amount",
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
                loan_date,
                monthly_collection,
                loan_amount,
                interest_rate,
                emi_amount
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                mobile,
                str(loan_date),
                monthly_collection,
                loan_amount,
                interest_rate,
                emi_amount
            )
        )

        conn.commit()

        st.success(
            "Customer Added Successfully"
        )

    st.divider()

    st.subheader("📋 Customer Records")

    st.dataframe(
        customers.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# MONTHLY COLLECTIONS
# =========================================

elif menu == "Monthly Collections":

    st.title("💵 Monthly Collections")

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
            INSERT INTO monthly_collections
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
# LOAN MANAGEMENT
# =========================================

elif menu == "Loan Management":

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

    loan_amount = customer["loan_amount"]

    principal_paid = principal_payments[
        principal_payments["customer_name"]
        ==
        customer_name
    ]["amount"].sum()

    remaining_balance = (
        loan_amount
        -
        principal_paid
    )

    st.metric(
        "🏦 Total Loan",
        f"₹ {loan_amount}"
    )

    st.metric(
        "💳 Principal Paid",
        f"₹ {principal_paid}"
    )

    st.metric(
        "📉 Remaining Balance",
        f"₹ {remaining_balance}"
    )

    st.divider()

    principal_amount = st.number_input(
        "Principal Amount Received",
        min_value=0.0
    )

    if st.button("Save Principal Payment"):

        c.execute(
            """
            INSERT INTO principal_payments
            (
                customer_name,
                amount,
                payment_date
            )
            VALUES (?, ?, ?)
            """,
            (
                customer_name,
                principal_amount,
                str(date.today())
            )
        )

        conn.commit()

        st.success(
            "Principal Payment Saved"
        )

    st.divider()

    st.dataframe(
        principal_payments.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# INTEREST MANAGEMENT
# =========================================

elif menu == "Interest Management":

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

    loan_amount = customer["loan_amount"]

    interest_rate = customer["interest_rate"]

    loan_date = datetime.strptime(
        customer["loan_date"],
        "%Y-%m-%d"
    ).date()

    today = date.today()

    months_passed = (
        (today.year - loan_date.year)
        * 12
        +
        (today.month - loan_date.month)
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

    pending_interest = (
        total_interest
        -
        interest_paid
    )

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
        "❌ Pending Interest",
        f"₹ {pending_interest}"
    )

    st.divider()

    interest_amount = st.number_input(
        "Interest Amount Received",
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
                interest_amount,
                str(date.today())
            )
        )

        conn.commit()

        st.success(
            "Interest Payment Saved"
        )

    st.divider()

    st.dataframe(
        interest_payments.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# PENDING COLLECTIONS
# =========================================

elif menu == "Pending Collections":

    st.title("❌ Pending Collections")

    selected_month = st.selectbox(
        "Select Month",
        month_options
    )

    paid_customers = []

    if not collections.empty:

        paid_data = collections[
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
        ]

        paid_customers = paid_data[
            "customer_name"
        ].tolist()

    pending_list = []

    for _, customer in customers.iterrows():

        start_date = datetime.strptime(
            customer["loan_date"],
            "%Y-%m-%d"
        )

        start_month = start_date.month

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
                    customer["monthly_collection"]
                })

    pending_df = pd.DataFrame(
        pending_list
    )

    total_pending = (
        pending_df[
            "Pending Amount"
        ].sum()
        if not pending_df.empty else 0
    )

    st.metric(
        "💵 Total Pending",
        f"₹ {total_pending}"
    )

    st.dataframe(
        pending_df.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# CUSTOMER PROFILE
# =========================================

elif menu == "Customer Profile":

    st.title("📜 Customer Profile")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    customer = customers[
        customers["name"]
        ==
        customer_name
    ].iloc[0]

    loan_amount = customer["loan_amount"]

    interest_rate = customer["interest_rate"]

    loan_date = datetime.strptime(
        customer["loan_date"],
        "%Y-%m-%d"
    ).date()

    today = date.today()

    months_passed = (
        (today.year - loan_date.year)
        * 12
        +
        (today.month - loan_date.month)
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

    pending_interest = (
        total_interest
        -
        interest_paid
    )

    principal_paid = principal_payments[
        principal_payments["customer_name"]
        ==
        customer_name
    ]["amount"].sum()

    remaining_balance = (
        loan_amount
        -
        principal_paid
    )

    total_due = (
        remaining_balance
        +
        pending_interest
    )

    st.subheader("📊 Loan Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏦 Loan Amount",
        f"₹ {loan_amount}"
    )

    col2.metric(
        "📈 Monthly Interest",
        f"₹ {monthly_interest}"
    )

    col3.metric(
        "💳 Remaining Balance",
        f"₹ {remaining_balance}"
    )

    col4.metric(
        "🔥 Total Due",
        f"₹ {total_due}"
    )

    st.divider()

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "📅 Months Passed",
        months_passed
    )

    col6.metric(
        "💰 Total Interest",
        f"₹ {total_interest}"
    )

    col7.metric(
        "❌ Pending Interest",
        f"₹ {pending_interest}"
    )

    st.divider()

    st.subheader("💵 Monthly Collection History")

    customer_collection = collections[
        collections["customer_name"]
        ==
        customer_name
    ]

    st.dataframe(
        customer_collection.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("📈 Interest Payment History")

    customer_interest = interest_payments[
        interest_payments["customer_name"]
        ==
        customer_name
    ]

    st.dataframe(
        customer_interest.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("🏦 Principal Payment History")

    customer_principal = principal_payments[
        principal_payments["customer_name"]
        ==
        customer_name
    ]

    st.dataframe(
        customer_principal.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# EXPENSES
# =========================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    expense_name = st.text_input(
        "Expense Name"
    )

    amount = st.number_input(
        "Expense Amount",
        min_value=0.0
    )

    if st.button("Add Expense"):

        c.execute(
            """
            INSERT INTO expenses
            (
                expense_name,
                amount,
                expense_date
            )
            VALUES (?, ?, ?)
            """,
            (
                expense_name,
                amount,
                str(date.today())
            )
        )

        conn.commit()

        st.success(
            "Expense Added"
        )

    st.divider()

    st.dataframe(
        expenses.reset_index(drop=True),
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

    st.subheader("📈 Interest Payments")

    st.dataframe(
        interest_payments.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("🏦 Principal Payments")

    st.dataframe(
        principal_payments.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("💸 Expenses")

    st.dataframe(
        expenses.reset_index(drop=True),
        use_container_width=True
    )

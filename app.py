import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Finance Loan Tracker Pro",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# DATABASE
# -----------------------------------

conn = sqlite3.connect(
    "tracker.db",
    check_same_thread=False
)

c = conn.cursor()

# -----------------------------------
# TABLES
# -----------------------------------

# Customers

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    start_date TEXT,
    loan_amount REAL,
    interest_rate REAL,
    emi_amount REAL
)
""")

# EMI Payments

c.execute("""
CREATE TABLE IF NOT EXISTS emi_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    month TEXT,
    emi_paid REAL,
    payment_date TEXT
)
""")

# Interest Payments

c.execute("""
CREATE TABLE IF NOT EXISTS interest_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    month TEXT,
    interest_paid REAL,
    payment_date TEXT
)
""")

# Principal Payments

c.execute("""
CREATE TABLE IF NOT EXISTS principal_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    principal_paid REAL,
    payment_date TEXT
)
""")

# Expenses

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT,
    amount REAL,
    expense_date TEXT
)
""")

conn.commit()

# -----------------------------------
# LOGIN
# -----------------------------------

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

VIEW_USER = "viewer"
VIEW_PASS = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# -----------------------------------
# LOGIN PAGE
# -----------------------------------

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

# -----------------------------------
# MONTHS
# -----------------------------------

month_options = [
    "January 2026",
    "February 2026",
    "March 2026",
    "April 2026",
    "May 2026",
    "June 2026",
    "July 2026",
    "August 2026",
    "September 2026",
    "October 2026",
    "November 2026",
    "December 2026"
]

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Add Customer",
        "EMI Payments",
        "Interest Payments",
        "Principal Payments",
        "Customer History",
        "Expenses",
        "Reports"
    ]
)

role = st.session_state.role

st.sidebar.write(
    f"👤 Logged in as: {role}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.rerun()

# -----------------------------------
# LOAD DATA
# -----------------------------------

customers = pd.read_sql(
    "SELECT * FROM customers",
    conn
)

emi_df = pd.read_sql(
    "SELECT * FROM emi_payments",
    conn
)

interest_df = pd.read_sql(
    "SELECT * FROM interest_payments",
    conn
)

principal_df = pd.read_sql(
    "SELECT * FROM principal_payments",
    conn
)

expenses = pd.read_sql(
    "SELECT * FROM expenses",
    conn
)

# -----------------------------------
# DASHBOARD
# -----------------------------------

if menu == "Dashboard":

    st.title("📊 Finance Dashboard")

    total_loan = (
        customers["loan_amount"].sum()
        if not customers.empty else 0
    )

    total_emi = (
        emi_df["emi_paid"].sum()
        if not emi_df.empty else 0
    )

    total_interest = (
        interest_df["interest_paid"].sum()
        if not interest_df.empty else 0
    )

    total_principal = (
        principal_df["principal_paid"].sum()
        if not principal_df.empty else 0
    )

    total_expense = (
        expenses["amount"].sum()
        if not expenses.empty else 0
    )

    remaining_loan = (
        total_loan
        -
        total_principal
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏦 Total Loan",
        f"₹ {total_loan}"
    )

    col2.metric(
        "💳 Principal Returned",
        f"₹ {total_principal}"
    )

    col3.metric(
        "📉 Remaining Loan",
        f"₹ {remaining_loan}"
    )

    col4.metric(
        "👥 Customers",
        len(customers)
    )

    st.divider()

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "💵 EMI Received",
        f"₹ {total_emi}"
    )

    col6.metric(
        "📈 Interest Received",
        f"₹ {total_interest}"
    )

    col7.metric(
        "💸 Expenses",
        f"₹ {total_expense}"
    )

    st.divider()

    st.subheader("👥 Customers")

    if customers.empty:

        st.warning("No Customers Found")

    else:

        st.dataframe(
            customers.reset_index(drop=True),
            use_container_width=True
        )

# -----------------------------------
# ADD CUSTOMER
# -----------------------------------

elif menu == "Add Customer":

    st.title("➕ Add Customer")

    if role != "admin":

        st.warning("View Only Access")
        st.stop()

    name = st.text_input("Customer Name")

    mobile = st.text_input("Mobile Number")

    start_date = st.date_input("Start Date")

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
        f"📈 Monthly Interest: ₹ {monthly_interest}"
    )

    if st.button("Save Customer"):

        c.execute(
            """
            INSERT INTO customers
            (
                name,
                mobile,
                start_date,
                loan_amount,
                interest_rate,
                emi_amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                mobile,
                str(start_date),
                loan_amount,
                interest_rate,
                emi_amount
            )
        )

        conn.commit()

        st.success(
            "Customer Added Successfully"
        )

# -----------------------------------
# EMI PAYMENTS
# -----------------------------------

elif menu == "EMI Payments":

    st.title("💵 EMI Payments")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    month = st.selectbox(
        "Select Month",
        month_options
    )

    emi_paid = st.number_input(
        "EMI Paid",
        min_value=0.0
    )

    if st.button("Save EMI Payment"):

        c.execute(
            """
            INSERT INTO emi_payments
            (
                customer_name,
                month,
                emi_paid,
                payment_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                customer_name,
                month,
                emi_paid,
                str(datetime.now().date())
            )
        )

        conn.commit()

        st.success("EMI Payment Saved")

    st.divider()

    st.dataframe(
        emi_df.reset_index(drop=True),
        use_container_width=True
    )

# -----------------------------------
# INTEREST PAYMENTS
# -----------------------------------

elif menu == "Interest Payments":

    st.title("📈 Interest Payments")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    month = st.selectbox(
        "Select Month",
        month_options
    )

    interest_paid = st.number_input(
        "Interest Paid",
        min_value=0.0
    )

    if st.button("Save Interest Payment"):

        c.execute(
            """
            INSERT INTO interest_payments
            (
                customer_name,
                month,
                interest_paid,
                payment_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                customer_name,
                month,
                interest_paid,
                str(datetime.now().date())
            )
        )

        conn.commit()

        st.success(
            "Interest Payment Saved"
        )

    st.divider()

    st.dataframe(
        interest_df.reset_index(drop=True),
        use_container_width=True
    )

# -----------------------------------
# PRINCIPAL PAYMENTS
# -----------------------------------

elif menu == "Principal Payments":

    st.title("🏦 Principal Payments")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    principal_paid = st.number_input(
        "Principal Amount Paid",
        min_value=0.0
    )

    if st.button("Save Principal Payment"):

        c.execute(
            """
            INSERT INTO principal_payments
            (
                customer_name,
                principal_paid,
                payment_date
            )
            VALUES (?, ?, ?)
            """,
            (
                customer_name,
                principal_paid,
                str(datetime.now().date())
            )
        )

        conn.commit()

        st.success(
            "Principal Payment Saved"
        )

    st.divider()

    st.dataframe(
        principal_df.reset_index(drop=True),
        use_container_width=True
    )

# -----------------------------------
# CUSTOMER HISTORY
# -----------------------------------

elif menu == "Customer History":

    st.title("📜 Customer History")

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    customer_data = customers[
        customers["name"]
        ==
        customer_name
    ].iloc[0]

    loan_amount = customer_data["loan_amount"]

    interest_rate = customer_data[
        "interest_rate"
    ]

    emi_amount = customer_data[
        "emi_amount"
    ]

    emi_history = emi_df[
        emi_df["customer_name"]
        ==
        customer_name
    ]

    interest_history = interest_df[
        interest_df["customer_name"]
        ==
        customer_name
    ]

    principal_history = principal_df[
        principal_df["customer_name"]
        ==
        customer_name
    ]

    total_emi = (
        emi_history["emi_paid"].sum()
        if not emi_history.empty else 0
    )

    total_interest = (
        interest_history[
            "interest_paid"
        ].sum()
        if not interest_history.empty else 0
    )

    total_principal = (
        principal_history[
            "principal_paid"
        ].sum()
        if not principal_history.empty else 0
    )

    remaining_loan = (
        loan_amount
        -
        total_principal
    )

    monthly_interest = (
        loan_amount
        *
        interest_rate
        / 100
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏦 Total Loan",
        f"₹ {loan_amount}"
    )

    col2.metric(
        "💳 Remaining Loan",
        f"₹ {remaining_loan}"
    )

    col3.metric(
        "📈 Monthly Interest",
        f"₹ {monthly_interest}"
    )

    col4.metric(
        "💵 EMI Amount",
        f"₹ {emi_amount}"
    )

    st.divider()

    st.subheader("👤 Customer Details")

    st.write(
        f"📱 Mobile: {customer_data['mobile']}"
    )

    st.write(
        f"📅 Start Date: {customer_data['start_date']}"
    )

    st.divider()

    st.subheader("💵 EMI History")

    st.dataframe(
        emi_history.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("📈 Interest History")

    st.dataframe(
        interest_history.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("🏦 Principal Payment History")

    st.dataframe(
        principal_history.reset_index(drop=True),
        use_container_width=True
    )

# -----------------------------------
# EXPENSES
# -----------------------------------

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
                str(datetime.now().date())
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

# -----------------------------------
# REPORTS
# -----------------------------------

elif menu == "Reports":

    st.title("📑 Reports")

    st.subheader("👥 Customer Report")

    st.dataframe(
        customers.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("💵 EMI Report")

    st.dataframe(
        emi_df.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("📈 Interest Report")

    st.dataframe(
        interest_df.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("🏦 Principal Report")

    st.dataframe(
        principal_df.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("💸 Expense Report")

    st.dataframe(
        expenses.reset_index(drop=True),
        use_container_width=True
    )

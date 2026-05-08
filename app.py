# =========================================================
# SMART FINANCE TRACKER PRO
# PROFESSIONAL FINAL VERSION
# =========================================================

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Finance Tracker Pro",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "tracker.db",
    check_same_thread=False
)

c = conn.cursor()

# =========================================================
# TABLES
# =========================================================

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    active INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    collection_start_date TEXT,
    monthly_collection REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    loan_amount REAL,
    interest_rate REAL,
    loan_start_date TEXT
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
CREATE TABLE IF NOT EXISTS principal_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT,
    amount REAL,
    donation_date TEXT,
    note TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT,
    amount REAL,
    expense_date TEXT,
    note TEXT
)
""")

# =========================================================
# DEFAULT ADMIN
# =========================================================

c.execute("""
INSERT OR IGNORE INTO users
(username, password, role, active)
VALUES
('admin', 'admin123', 'admin', 1)
""")

conn.commit()

# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = c.execute(
            """
            SELECT * FROM users
            WHERE username=?
            AND password=?
            AND active=1
            """,
            (
                username,
                password
            )
        ).fetchone()

        if user:

            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]

            st.rerun()

        else:

            st.error("Invalid Login")

    st.stop()

# =========================================================
# LOAD DATA
# =========================================================

customers = pd.read_sql(
    "SELECT * FROM customers",
    conn
)

loans = pd.read_sql(
    "SELECT * FROM loans",
    conn
)

collections = pd.read_sql(
    "SELECT * FROM collections",
    conn
)

principal_payments = pd.read_sql(
    "SELECT * FROM principal_payments",
    conn
)

donations = pd.read_sql(
    "SELECT * FROM donations",
    conn
)

expenses = pd.read_sql(
    "SELECT * FROM expenses",
    conn
)

users = pd.read_sql(
    "SELECT * FROM users",
    conn
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 Menu")

menu_options = [
    "Dashboard",
    "Customers",
    "Monthly Collections",
    "Start Loan",
    "Loan Management",
    "Donations",
    "Expenses",
    "Pending Collections",
    "Reports"
]

if st.session_state.role == "admin":
    menu_options.append("User Management")

menu = st.sidebar.radio(
    "Select Option",
    menu_options
)

st.sidebar.write(
    f"👤 {st.session_state.username}"
)

st.sidebar.write(
    f"🔐 {st.session_state.role}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.rerun()

# =========================================================
# PERMISSION
# =========================================================

can_edit = (
    st.session_state.role
    in
    ["admin", "editor"]
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.title("📊 Finance Dashboard")

    total_collection = (
        collections["amount"].sum()
        if not collections.empty else 0
    )

    total_loan = (
        loans["loan_amount"].sum()
        if not loans.empty else 0
    )

    total_returned = (
        principal_payments["amount"].sum()
        if not principal_payments.empty else 0
    )

    total_donation = (
        donations["amount"].sum()
        if not donations.empty else 0
    )

    total_expense = (
        expenses["amount"].sum()
        if not expenses.empty else 0
    )

    remaining_loan = (
        total_loan
        -
        total_returned
    )

    final_balance = (
        total_collection
        +
        total_donation
        -
        total_expense
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💵 Collections",
        f"₹ {total_collection}"
    )

    col2.metric(
        "🏦 Loan Given",
        f"₹ {total_loan}"
    )

    col3.metric(
        "💳 Returned",
        f"₹ {total_returned}"
    )

    st.divider()

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "🎁 Donations",
        f"₹ {total_donation}"
    )

    col5.metric(
        "💸 Expenses",
        f"₹ {total_expense}"
    )

    col6.metric(
        "💰 Balance",
        f"₹ {final_balance}"
    )

    st.divider()

    st.metric(
        "📉 Remaining Loan",
        f"₹ {remaining_loan}"
    )

# =========================================================
# CUSTOMERS
# =========================================================

elif menu == "Customers":

    st.title("👥 Customers")

    if can_edit:

        name = st.text_input("Customer Name")

        mobile = st.text_input("Mobile")

        start_date = st.date_input(
            "Collection Start Date"
        )

        monthly_collection = st.number_input(
            "Monthly Collection",
            min_value=0.0
        )

        if st.button("Save Customer"):

            c.execute(
                """
                INSERT INTO customers
                (
                    name,
                    mobile,
                    collection_start_date,
                    monthly_collection
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    mobile,
                    str(start_date),
                    monthly_collection
                )
            )

            conn.commit()

            st.success("Customer Added")

    st.divider()

    st.dataframe(
        customers,
        use_container_width=True
    )

# =========================================================
# MONTHLY COLLECTIONS
# =========================================================

elif menu == "Monthly Collections":

    st.title("💵 Monthly Collections")

    if not customers.empty:

        customer_name = st.selectbox(
            "Customer",
            customers["name"]
        )

        month = st.text_input(
            "Month"
        )

        amount = st.number_input(
            "Amount",
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

        payment_date = st.date_input(
            "Payment Date"
        )

        if can_edit:

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
                        str(payment_date)
                    )
                )

                conn.commit()

                st.success("Collection Saved")

    st.divider()

    st.dataframe(
        collections,
        use_container_width=True
    )

# =========================================================
# START LOAN
# =========================================================

elif menu == "Start Loan":

    st.title("🏦 Start Loan")

    if not customers.empty:

        customer_name = st.selectbox(
            "Customer",
            customers["name"]
        )

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0.0
        )

        interest_rate = st.number_input(
            "Monthly Interest %",
            min_value=0.0
        )

        loan_date = st.date_input(
            "Loan Date"
        )

        if can_edit:

            if st.button("Start Loan"):

                c.execute(
                    """
                    INSERT INTO loans
                    (
                        customer_name,
                        loan_amount,
                        interest_rate,
                        loan_start_date
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        customer_name,
                        loan_amount,
                        interest_rate,
                        str(loan_date)
                    )
                )

                conn.commit()

                st.success("Loan Started")

# =========================================================
# LOAN MANAGEMENT
# =========================================================

elif menu == "Loan Management":

    st.title("🏦 Loan Management")

    if not loans.empty:

        customer_name = st.selectbox(
            "Select Customer",
            loans["customer_name"].unique()
        )

        loan_data = loans[
            loans["customer_name"]
            ==
            customer_name
        ].iloc[0]

        original_loan = float(
            loan_data["loan_amount"]
        )

        interest_rate = float(
            loan_data["interest_rate"]
        )

        payments = principal_payments[
            principal_payments["customer_name"]
            ==
            customer_name
        ]

        returned = (
            payments["amount"].sum()
            if not payments.empty else 0
        )

        remaining = (
            original_loan
            -
            returned
        )

        monthly_interest = (
            remaining
            *
            interest_rate
            / 100
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🏦 Original Loan",
            f"₹ {original_loan}"
        )

        col2.metric(
            "💳 Returned",
            f"₹ {returned}"
        )

        col3.metric(
            "📉 Remaining",
            f"₹ {remaining}"
        )

        col4.metric(
            "📈 Monthly Interest",
            f"₹ {monthly_interest}"
        )

        st.divider()

        if can_edit:

            return_amount = st.number_input(
                "Return Amount",
                min_value=0.0
            )

            return_date = st.date_input(
                "Return Date"
            )

            if st.button("Save Return"):

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
                        return_amount,
                        str(return_date)
                    )
                )

                conn.commit()

                st.success("Return Saved")

        st.divider()

        st.subheader("📋 Return History")

        st.dataframe(
            payments,
            use_container_width=True
        )

# =========================================================
# DONATIONS
# =========================================================

elif menu == "Donations":

    st.title("🎁 Donations")

    donor_name = st.text_input(
        "Donor Name"
    )

    donation_amount = st.number_input(
        "Donation Amount",
        min_value=0.0
    )

    donation_date = st.date_input(
        "Donation Date"
    )

    donation_note = st.text_area(
        "Comment / Note"
    )

    if can_edit:

        if st.button("Save Donation"):

            c.execute(
                """
                INSERT INTO donations
                (
                    donor_name,
                    amount,
                    donation_date,
                    note
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    donor_name,
                    donation_amount,
                    str(donation_date),
                    donation_note
                )
            )

            conn.commit()

            st.success("Donation Saved")

    st.divider()

    st.dataframe(
        donations,
        use_container_width=True
    )

# =========================================================
# EXPENSES
# =========================================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    expense_name = st.text_input(
        "Expense Name"
    )

    expense_amount = st.number_input(
        "Expense Amount",
        min_value=0.0
    )

    expense_date = st.date_input(
        "Expense Date"
    )

    expense_note = st.text_area(
        "Comment / Note"
    )

    if can_edit:

        if st.button("Save Expense"):

            c.execute(
                """
                INSERT INTO expenses
                (
                    expense_name,
                    amount,
                    expense_date,
                    note
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    expense_name,
                    expense_amount,
                    str(expense_date),
                    expense_note
                )
            )

            conn.commit()

            st.success("Expense Saved")

    st.divider()

    st.dataframe(
        expenses,
        use_container_width=True
    )

# =========================================================
# PENDING COLLECTIONS
# =========================================================

elif menu == "Pending Collections":

    st.title("❌ Pending Collections")

    pending = collections[
        collections["status"]
        !=
        "Paid"
    ]

    st.dataframe(
        pending,
        use_container_width=True
    )

# =========================================================
# USER MANAGEMENT
# =========================================================

elif menu == "User Management":

    st.title("👤 User Management")

    username = st.text_input(
        "New Username"
    )

    password = st.text_input(
        "New Password"
    )

    role = st.selectbox(
        "Role",
        [
            "editor",
            "viewer"
        ]
    )

    if st.button("Create User"):

        try:

            c.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    role,
                    active
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    password,
                    role,
                    1
                )
            )

            conn.commit()

            st.success("User Created")

        except:

            st.error("User Already Exists")

    st.divider()

    st.subheader("📋 Users")

    st.dataframe(
        users,
        use_container_width=True
    )

# =========================================================
# REPORTS
# =========================================================

elif menu == "Reports":

    st.title("📑 Professional Reports")

    total_collection = (
        collections["amount"].sum()
        if not collections.empty else 0
    )

    total_loan = (
        loans["loan_amount"].sum()
        if not loans.empty else 0
    )

    total_returned = (
        principal_payments["amount"].sum()
        if not principal_payments.empty else 0
    )

    total_donation = (
        donations["amount"].sum()
        if not donations.empty else 0
    )

    total_expense = (
        expenses["amount"].sum()
        if not expenses.empty else 0
    )

    remaining_loan = (
        total_loan
        -
        total_returned
    )

    final_balance = (
        total_collection
        +
        total_donation
        -
        total_expense
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Collections",
        f"₹ {total_collection}"
    )

    col2.metric(
        "🏦 Loan",
        f"₹ {total_loan}"
    )

    col3.metric(
        "💳 Returned",
        f"₹ {total_returned}"
    )

    col4.metric(
        "📉 Remaining",
        f"₹ {remaining_loan}"
    )

    st.divider()

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "🎁 Donations",
        f"₹ {total_donation}"
    )

    col6.metric(
        "💸 Expenses",
        f"₹ {total_expense}"
    )

    col7.metric(
        "💰 Balance",
        f"₹ {final_balance}"
    )

    st.divider()

    st.subheader("👥 Customer Report")

    customer_report = []

    for _, row in loans.iterrows():

        customer = row["customer_name"]

        loan_amount = row["loan_amount"]

        rate = row["interest_rate"]

        paid = principal_payments[
            principal_payments["customer_name"]
            ==
            customer
        ]["amount"].sum()

        remaining = loan_amount - paid

        interest = (
            remaining
            *
            rate
            / 100
        )

        customer_report.append(
            {
                "Customer": customer,
                "Loan": loan_amount,
                "Returned": paid,
                "Remaining": remaining,
                "Interest": interest
            }
        )

    customer_df = pd.DataFrame(
        customer_report
    )

    st.dataframe(
        customer_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("🎁 Donation Report")

    st.dataframe(
        donations,
        use_container_width=True
    )

    st.divider()

    st.subheader("💸 Expense Report")

    st.dataframe(
        expenses,
        use_container_width=True
    )

    st.divider()

    st.subheader("💵 Collection Report")

    st.dataframe(
        collections,
        use_container_width=True
    )

    st.divider()

    st.subheader("🏦 Loan Ledger")

    ledger = []

    for _, row in loans.iterrows():

        ledger.append(
            {
                "Date": row["loan_start_date"],
                "Action": "Loan Given",
                "Customer": row["customer_name"],
                "Amount": row["loan_amount"]
            }
        )

    for _, row in principal_payments.iterrows():

        ledger.append(
            {
                "Date": row["payment_date"],
                "Action": "Returned",
                "Customer": row["customer_name"],
                "Amount": row["amount"]
            }
        )

    ledger_df = pd.DataFrame(
        ledger
    )

    st.dataframe(
        ledger_df,
        use_container_width=True
    )

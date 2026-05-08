# =========================================================
# SMART FINANCE TRACKER PRO
# FULL FINAL VERSION
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

# USERS

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    active INTEGER
)
""")

# CUSTOMERS

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    collection_start_date TEXT,
    monthly_collection REAL
)
""")

# LOANS

c.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    loan_amount REAL,
    interest_rate REAL,
    loan_start_date TEXT
)
""")

# COLLECTIONS

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

# PRINCIPAL PAYMENTS

c.execute("""
CREATE TABLE IF NOT EXISTS principal_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_date TEXT
)
""")

# DONATIONS

c.execute("""
CREATE TABLE IF NOT EXISTS donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT,
    amount REAL,
    donation_date TEXT,
    note TEXT
)
""")

# EXPENSES

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT,
    amount REAL,
    expense_date TEXT,
    note TEXT
)
""")

# DEFAULT ADMIN

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
# MONTHS
# =========================================================

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

    menu_options.append(
        "User Management"
    )

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
# PERMISSIONS
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

    total_donation = (
        donations["amount"].sum()
        if not donations.empty else 0
    )

    total_expense = (
        expenses["amount"].sum()
        if not expenses.empty else 0
    )

    total_loan = (
        loans["loan_amount"].sum()
        if not loans.empty else 0
    )

    total_returned = (
        principal_payments["amount"].sum()
        if not principal_payments.empty else 0
    )

    remaining_loan = (
        total_loan
        -
        total_returned
    )

    remaining_balance = (
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
        "🎁 Donations",
        f"₹ {total_donation}"
    )

    col3.metric(
        "💸 Expenses",
        f"₹ {total_expense}"
    )

    st.divider()

    col4, col5 = st.columns(2)

    col4.metric(
        "🏦 Remaining Loan",
        f"₹ {remaining_loan}"
    )

    col5.metric(
        "💰 Remaining Balance",
        f"₹ {remaining_balance}"
    )

# =========================================================
# CUSTOMERS
# =========================================================

elif menu == "Customers":

    st.title("👥 Customers")

    if can_edit:

        name = st.text_input(
            "Customer Name"
        )

        mobile = st.text_input(
            "Mobile Number"
        )

        collection_start_date = st.date_input(
            "Collection Start Date"
        )

        monthly_collection = st.number_input(
            "Monthly Collection Amount",
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
                    str(collection_start_date),
                    monthly_collection
                )
            )

            conn.commit()

            st.success("Customer Added")

    else:

        st.warning("Viewer Access Only")

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

    if can_edit:

        customer_name = st.selectbox(
            "Select Customer",
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

        loan_start_date = st.date_input(
            "Loan Start Date"
        )

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
                    str(loan_start_date)
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

        current_interest = (
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
            "📈 Interest",
            f"₹ {current_interest}"
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

    st.subheader("➕ Create User")

    new_username = st.text_input(
        "New Username"
    )

    new_password = st.text_input(
        "New Password"
    )

    new_role = st.selectbox(
        "Select Role",
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
                    new_username,
                    new_password,
                    new_role,
                    1
                )
            )

            conn.commit()

            st.success(
                "User Created"
            )

        except:

            st.error(
                "Username Already Exists"
            )

    st.divider()

    st.subheader("📋 All Users")

    users_display = pd.read_sql(
        """
        SELECT
        username,
        role,
        active
        FROM users
        """,
        conn
    )

    users_display["active"] = users_display[
        "active"
    ].replace(
        {
            1: "Active",
            0: "Disabled"
        }
    )

    st.dataframe(
        users_display,
        use_container_width=True
    )

# =========================================================
# REPORTS
# =========================================================

elif menu == "Reports":

    st.title("📑 Reports")

    st.subheader("👥 Customers")
    st.dataframe(customers)

    st.subheader("🏦 Loans")
    st.dataframe(loans)

    st.subheader("💵 Collections")
    st.dataframe(collections)

    st.subheader("💳 Returns")
    st.dataframe(principal_payments)

    st.subheader("🎁 Donations")
    st.dataframe(donations)

    st.subheader("💸 Expenses")
    st.dataframe(expenses)

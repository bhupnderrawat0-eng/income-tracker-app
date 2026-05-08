# =========================================================
# SMART FINANCE TRACKER PRO
# MULTI USER + ROLE BASED SYSTEM
# =========================================================

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

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
# CREATE TABLES
# =========================================================

# USERS TABLE

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    active INTEGER
)
""")

# DEFAULT ADMIN

c.execute("""
INSERT OR IGNORE INTO users
(username, password, role, active)
VALUES
('admin', 'admin123', 'admin', 1)
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

# INTEREST PAYMENTS

c.execute("""
CREATE TABLE IF NOT EXISTS interest_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount REAL,
    payment_date TEXT
)
""")

conn.commit()

# =========================================================
# LOGIN SYSTEM
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input(
        "Username"
    )

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

            st.error(
                "Invalid Credentials"
            )

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

interest_payments = pd.read_sql(
    "SELECT * FROM interest_payments",
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
    "Pending Collections",
    "Reports"
]

# ONLY ADMIN CAN SEE USER MANAGEMENT

if st.session_state.role == "admin":

    menu_options.append(
        "User Management"
    )

menu = st.sidebar.radio(
    "Select Option",
    menu_options
)

st.sidebar.write(
    f"👤 User: {st.session_state.username}"
)

st.sidebar.write(
    f"🔐 Role: {st.session_state.role}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()

# =========================================================
# ROLE PERMISSION
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

    st.title("📊 Dashboard")

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

    remaining_loan = (
        total_loan
        -
        total_returned
    )

    total_interest = (
        interest_payments["amount"].sum()
        if not interest_payments.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Collections",
        f"₹ {total_collection}"
    )

    col2.metric(
        "🏦 Total Loan",
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

    st.metric(
        "📈 Interest Received",
        f"₹ {total_interest}"
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

            st.success(
                "Customer Added"
            )

    else:

        st.warning(
            "View Only Access"
        )

    st.divider()

    st.dataframe(
        customers.reset_index(drop=True),
        use_container_width=True
    )

# =========================================================
# MONTHLY COLLECTIONS
# =========================================================

elif menu == "Monthly Collections":

    st.title("💵 Monthly Collections")

    if customers.empty:

        st.warning("No Customers")

    else:

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

                st.success(
                    "Collection Saved"
                )

        else:

            st.warning(
                "View Only Access"
            )

        st.divider()

        st.dataframe(
            collections.reset_index(drop=True),
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
            "Monthly Interest Rate (%)",
            min_value=0.0
        )

        loan_start_date = st.date_input(
            "Loan Start Date"
        )

        monthly_interest = (
            loan_amount
            *
            interest_rate
            / 100
        )

        st.info(
            f"Monthly Interest = ₹ {monthly_interest}"
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

            st.success(
                "Loan Started"
            )

    else:

        st.warning(
            "View Only Access"
        )

# =========================================================
# LOAN MANAGEMENT
# =========================================================

elif menu == "Loan Management":

    st.title("🏦 Loan Management")

    if loans.empty:

        st.warning(
            "No Loans Found"
        )

    else:

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

        payment_history = principal_payments[
            principal_payments["customer_name"]
            ==
            customer_name
        ]

        total_returned = (
            payment_history["amount"].sum()
            if not payment_history.empty else 0
        )

        remaining = (
            original_loan
            -
            total_returned
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
            f"₹ {total_returned}"
        )

        col3.metric(
            "📉 Remaining",
            f"₹ {remaining}"
        )

        col4.metric(
            "📈 Current Interest",
            f"₹ {current_interest}"
        )

        st.divider()

        if can_edit:

            return_amount = st.number_input(
                "Principal Return Amount",
                min_value=0.0
            )

            return_date = st.date_input(
                "Return Date"
            )

            if st.button(
                "Save Principal Return"
            ):

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

                st.success(
                    "Return Saved"
                )

        st.divider()

        st.subheader(
            "📋 Return History"
        )

        st.dataframe(
            payment_history.reset_index(drop=True),
            use_container_width=True
        )

# =========================================================
# PENDING COLLECTIONS
# =========================================================

elif menu == "Pending Collections":

    st.title("❌ Pending Collections")

    selected_month = st.selectbox(
        "Select Month",
        month_options
    )

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

    pending_list = []

    for _, customer in customers.iterrows():

        start_date = datetime.strptime(
            customer["collection_start_date"],
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

    st.dataframe(
        pending_df.reset_index(drop=True),
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

    st.dataframe(
        users.reset_index(drop=True),
        use_container_width=True
    )

    st.divider()

    st.subheader("🚫 Disable User")

    disable_user = st.selectbox(
        "Select User",
        users["username"]
    )

    if st.button("Disable User"):

        c.execute(
            """
            UPDATE users
            SET active=0
            WHERE username=?
            """,
            (disable_user,)
        )

        conn.commit()

        st.success(
            "User Disabled"
        )

# =========================================================
# REPORTS
# =========================================================

elif menu == "Reports":

    st.title("📑 Reports")

    st.subheader("👥 Customers")

    st.dataframe(
        customers.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("🏦 Loans")

    st.dataframe(
        loans.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("💵 Collections")

    st.dataframe(
        collections.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("💳 Principal Returns")

    st.dataframe(
        principal_payments.reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("📈 Interest Payments")

    st.dataframe(
        interest_payments.reset_index(drop=True),
        use_container_width=True
    )

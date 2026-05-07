import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------
st.set_page_config(
    page_title="Income Tracker Pro",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
conn = sqlite3.connect(
    "tracker.db",
    check_same_thread=False
)

c = conn.cursor()

# -----------------------------------
# CREATE TABLES
# -----------------------------------

# Customers Table
c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    start_date TEXT,
    monthly_amount REAL
)
""")

# Receipts Table
c.execute("""
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    month TEXT,
    amount REAL,
    status TEXT
)
""")

# Expenses Table
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
# MONTH OPTIONS
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
# LOGIN SYSTEM
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
# SIDEBAR
# -----------------------------------

st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Add Customer",
        "Monthly Received",
        "Pending Customers",
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

receipts = pd.read_sql(
    "SELECT * FROM receipts",
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

    st.title("📊 Dashboard")

    dashboard_view = st.radio(
        "Select View",
        ["Overall", "Month Wise"],
        horizontal=True
    )

    # -----------------------------------
    # OVERALL VIEW
    # -----------------------------------

    if dashboard_view == "Overall":

        total_received = (
            receipts["amount"].sum()
            if not receipts.empty else 0
        )

        total_expense = (
            expenses["amount"].sum()
            if not expenses.empty else 0
        )

        balance = (
            total_received
            -
            total_expense
        )

        total_customers = len(customers)

        received_customers = []

        if not receipts.empty:

            received_customers = receipts[
                receipts["status"] == "Received"
            ]["customer_name"].unique().tolist()

        pending_customers = (
            total_customers
            -
            len(received_customers)
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "👥 Total Customers",
            total_customers
        )

        col2.metric(
            "💰 Total Received",
            f"₹ {total_received}"
        )

        col3.metric(
            "💸 Total Expense",
            f"₹ {total_expense}"
        )

        col4.metric(
            "❌ Pending Customers",
            pending_customers
        )

        st.divider()

        st.metric(
            "🏦 Remaining Balance",
            f"₹ {balance}"
        )

    # -----------------------------------
    # MONTH WISE VIEW
    # -----------------------------------

    else:

        selected_month = st.selectbox(
            "📅 Select Month",
            month_options,
            index=4
        )

        month_receipts = pd.DataFrame()

        if not receipts.empty:

            month_receipts = receipts[
                receipts["month"] == selected_month
            ]

        total_received = (
            month_receipts["amount"].sum()
            if not month_receipts.empty else 0
        )

        total_expense = (
            expenses["amount"].sum()
            if not expenses.empty else 0
        )

        balance = (
            total_received
            -
            total_expense
        )

        received_customers = []

        if not month_receipts.empty:

            received_customers = month_receipts[
                month_receipts["status"] == "Received"
            ]["customer_name"].tolist()

        pending_customers = []

        for customer in customers["name"]:

            if customer not in received_customers:

                pending_customers.append(customer)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "👥 Total Customers",
            len(customers)
        )

        col2.metric(
            "💰 Month Received",
            f"₹ {total_received}"
        )

        col3.metric(
            "💸 Total Expense",
            f"₹ {total_expense}"
        )

        col4.metric(
            "❌ Pending Customers",
            len(pending_customers)
        )

        st.divider()

        st.metric(
            "🏦 Remaining Balance",
            f"₹ {balance}"
        )

        # Paid Customers

        st.subheader("✅ Customers Who Paid")

        paid_df = pd.DataFrame()

        if not month_receipts.empty:

            paid_df = month_receipts[
                month_receipts["status"]
                ==
                "Received"
            ]

        if paid_df.empty:

            st.warning("No Received Payments")

        else:

            st.dataframe(
                paid_df.reset_index(drop=True),
                use_container_width=True
            )

        # Pending Customers

        st.subheader("❌ Pending Customers")

        pending_list = []

        for _, row in customers.iterrows():

            customer_name = row["name"]

            if customer_name not in received_customers:

                pending_list.append({

                    "Customer Name":
                    customer_name,

                    "Monthly Amount":
                    row["monthly_amount"],

                    "Status":
                    "Pending"
                })

        pending_df = pd.DataFrame(
            pending_list
        )

        if pending_df.empty:

            st.success("All Customers Paid")

        else:

            st.dataframe(
                pending_df.reset_index(drop=True),
                use_container_width=True
            )

    st.divider()

    st.subheader("👥 Customer List")

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

    start_date = st.date_input("Start Date")

    monthly_amount = st.number_input(
        "Monthly Amount",
        min_value=0.0
    )

    if st.button("Save Customer"):

        if name == "":

            st.error(
                "Please Enter Customer Name"
            )

        else:

            c.execute(
                """
                INSERT INTO customers
                (name, start_date, monthly_amount)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    str(start_date),
                    monthly_amount
                )
            )

            conn.commit()

            st.success(
                "Customer Added Successfully"
            )

# -----------------------------------
# MONTHLY RECEIVED
# -----------------------------------

elif menu == "Monthly Received":

    st.title("💵 Monthly Received")

    if customers.empty:

        st.warning("No Customers Found")
        st.stop()

    customer_name = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    month = st.selectbox(
        "Select Month",
        month_options,
        index=4
    )

    amount = st.number_input(
        "Amount Received",
        min_value=0.0
    )

    status = st.selectbox(
        "Status",
        [
            "Received",
            "Pending",
            "Partial"
        ]
    )

    if role == "admin":

        if st.button("Save Record"):

            c.execute(
                """
                INSERT INTO receipts
                (customer_name, month, amount, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    customer_name,
                    month,
                    amount,
                    status
                )
            )

            conn.commit()

            st.success(
                "Record Saved Successfully"
            )

    else:

        st.warning("View Only Access")

    st.divider()

    st.subheader("📋 All Records")

    if receipts.empty:

        st.warning("No Records Found")

    else:

        st.dataframe(
            receipts.reset_index(drop=True),
            use_container_width=True
        )

# -----------------------------------
# PENDING CUSTOMERS
# -----------------------------------

elif menu == "Pending Customers":

    st.title("❌ Pending Customers")

    selected_month = st.selectbox(
        "📅 Select Month",
        month_options,
        index=4
    )

    received_customers = []

    if not receipts.empty:

        month_data = receipts[
            (receipts["month"] == selected_month)
            &
            (receipts["status"] == "Received")
        ]

        received_customers = month_data[
            "customer_name"
        ].tolist()

    pending_list = []

    for _, row in customers.iterrows():

        customer_name = row["name"]

        if customer_name not in received_customers:

            pending_list.append({

                "Customer Name":
                customer_name,

                "Monthly Amount":
                row["monthly_amount"],

                "Status":
                "Pending"
            })

    pending_df = pd.DataFrame(
        pending_list
    )

    if pending_df.empty:

        st.success("All Customers Paid")

    else:

        st.dataframe(
            pending_df.reset_index(drop=True),
            use_container_width=True
        )

# -----------------------------------
# CUSTOMER HISTORY
# -----------------------------------

elif menu == "Customer History":

    st.title("📜 Customer History")

    if customers.empty:

        st.warning("No Customers Found")
        st.stop()

    selected_customer = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    customer_history = receipts[
        receipts["customer_name"]
        ==
        selected_customer
    ]

    if customer_history.empty:

        st.warning("No Records Found")

    else:

        total_received = customer_history[
            "amount"
        ].sum()

        st.metric(
            "💰 Total Received",
            f"₹ {total_received}"
        )

        st.dataframe(
            customer_history.reset_index(drop=True),
            use_container_width=True
        )

# -----------------------------------
# EXPENSES
# -----------------------------------

elif menu == "Expenses":

    st.title("💸 Expenses")

    if role == "admin":

        expense_name = st.text_input(
            "Expense Name"
        )

        amount = st.number_input(
            "Expense Amount",
            min_value=0.0
        )

        if st.button("Add Expense"):

            if expense_name == "":

                st.error(
                    "Please Enter Expense Name"
                )

            else:

                c.execute(
                    """
                    INSERT INTO expenses
                    (expense_name, amount, expense_date)
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
                    "Expense Added Successfully"
                )

    else:

        st.warning("View Only Access")

    st.divider()

    st.subheader("📋 Expense Records")

    if expenses.empty:

        st.warning(
            "No Expense Records Found"
        )

    else:

        st.dataframe(
            expenses.reset_index(drop=True),
            use_container_width=True
        )

# -----------------------------------
# REPORTS
# -----------------------------------

elif menu == "Reports":

    st.title("📑 Reports")

    selected_month = st.selectbox(
        "📅 Select Report Month",
        month_options,
        index=4
    )

    total_received = (
        receipts["amount"].sum()
        if not receipts.empty else 0
    )

    total_expense = (
        expenses["amount"].sum()
        if not expenses.empty else 0
    )

    balance = (
        total_received
        -
        total_expense
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Received",
        f"₹ {total_received}"
    )

    col2.metric(
        "💸 Total Expense",
        f"₹ {total_expense}"
    )

    col3.metric(
        "🏦 Remaining Balance",
        f"₹ {balance}"
    )

    st.divider()

    # Paid Customers

    st.subheader("✅ Customers Who Paid")

    paid_df = pd.DataFrame()

    if not receipts.empty:

        paid_df = receipts[
            (receipts["month"] == selected_month)
            &
            (receipts["status"] == "Received")
        ]

    if paid_df.empty:

        st.warning("No Received Payments")

    else:

        st.dataframe(
            paid_df.reset_index(drop=True),
            use_container_width=True
        )

    # Pending Customers

    st.subheader("❌ Customers Pending")

    received_customers = []

    if not receipts.empty:

        month_data = receipts[
            (receipts["month"] == selected_month)
            &
            (receipts["status"] == "Received")
        ]

        received_customers = month_data[
            "customer_name"
        ].tolist()

    pending_list = []

    for _, row in customers.iterrows():

        customer_name = row["name"]

        if customer_name not in received_customers:

            pending_list.append({

                "Customer Name":
                customer_name,

                "Monthly Amount":
                row["monthly_amount"],

                "Status":
                "Pending"
            })

    pending_df = pd.DataFrame(
        pending_list
    )

    if pending_df.empty:

        st.success("No Pending Customers")

    else:

        st.dataframe(
            pending_df.reset_index(drop=True),
            use_container_width=True
        )

    st.divider()

    # Expense Records

    st.subheader("💸 Expense Records")

    if expenses.empty:

        st.warning(
            "No Expense Records Found"
        )

    else:

        st.dataframe(
            expenses.reset_index(drop=True),
            use_container_width=True
        )
import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Finance Tracker Pro",
    layout="wide"
)

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
# LOGIN
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

    st.title("🔐 Login")

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

st.sidebar.title("📌 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Customers",
        "Monthly Collections",
        "Start Loan",
        "Loan Management",
        "Donations",
        "Expenses",
        "Pending Collections",
        "Reports",
        "User Management"
    ]
)

st.sidebar.write("👤", st.session_state.username)
st.sidebar.write("🔐", st.session_state.role)

if st.sidebar.button("Logout"):

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

    c1, c2, c3 = st.columns(3)

    c1.metric("💵 Collections", f"₹ {collections_total}")
    c2.metric("🎁 Donations", f"₹ {donations_total}")
    c3.metric("💸 Expenses", f"₹ {expenses_total}")

    c4, c5 = st.columns(2)

    c4.metric("🏦 Remaining Loan", f"₹ {remaining_loans}")
    c5.metric("🪙 Remaining Balance", f"₹ {balance}")

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
# MONTHLY COLLECTIONS
# =====================================================

elif menu == "Monthly Collections":

    st.title("💵 Monthly Collections")

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
# START LOAN
# =====================================================

elif menu == "Start Loan":

    st.title("🏦 Start Loan")

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

# =====================================================
# LOAN MANAGEMENT
# =====================================================

elif menu == "Loan Management":

    st.title("🏢 Loan Management")

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

        st.divider()

        st.subheader("💵 Add Principal Return")

        return_amount = st.number_input(
            "Return Amount",
            min_value=0.0
        )

        return_date = st.date_input(
            "Return Date"
        )

        if st.button("Save Return"):

            loan["returned"] += return_amount

            st.success("Return Saved")

# =====================================================
# DONATIONS
# =====================================================

elif menu == "Donations":

    st.title("🎁 Donations")

    donor_name = st.text_input("Donor Name")

    donation_amount = st.number_input(
        "Donation Amount",
        min_value=0.0
    )

    note = st.text_area("Comment / Note")

    donation_date = st.date_input("Donation Date")

    if st.button("Save Donation"):

        st.session_state.donations.append({
            "name": donor_name,
            "amount": donation_amount,
            "note": note,
            "date": str(donation_date)
        })

        st.success("Donation Saved")

    if st.session_state.donations:

        df = pd.DataFrame(st.session_state.donations)

        st.dataframe(df, use_container_width=True)

# =====================================================
# EXPENSES
# =====================================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    expense_title = st.text_input("Expense Title")

    expense_amount = st.number_input(
        "Expense Amount",
        min_value=0.0
    )

    expense_note = st.text_area("Expense Note")

    expense_date = st.date_input("Expense Date")

    if st.button("Save Expense"):

        st.session_state.expenses.append({
            "title": expense_title,
            "amount": expense_amount,
            "note": expense_note,
            "date": str(expense_date)
        })

        st.success("Expense Saved")

    if st.session_state.expenses:

        df = pd.DataFrame(st.session_state.expenses)

        st.dataframe(df, use_container_width=True)

# =====================================================
# PENDING COLLECTIONS
# =====================================================

elif menu == "Pending Collections":

    st.title("⏳ Pending Collections")

    pending = [
        x for x in st.session_state.collections
        if x["status"] == "Pending"
    ]

    if pending:

        df = pd.DataFrame(pending)

        st.dataframe(df, use_container_width=True)

    else:

        st.success("No Pending Collections")

# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":

    st.header("📊 Reports Dashboard")

    collections_df = pd.DataFrame(st.session_state.collections)
    loans_df = pd.DataFrame(st.session_state.loans)
    expenses_df = pd.DataFrame(st.session_state.expenses)
    donations_df = pd.DataFrame(st.session_state.donations)

    total_collections = (
        collections_df["amount"].sum()
        if not collections_df.empty else 0
    )

    total_loans = (
        loans_df["loan_amount"].sum()
        if not loans_df.empty else 0
    )

    returned_loans = (
        loans_df["returned"].sum()
        if not loans_df.empty else 0
    )

    pending_loans = total_loans - returned_loans

    total_expenses = (
        expenses_df["amount"].sum()
        if not expenses_df.empty else 0
    )

    total_donations = (
        donations_df["amount"].sum()
        if not donations_df.empty else 0
    )

    net_balance = (
        total_collections
        + total_donations
        - total_expenses
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("💰 Collections", f"₹ {total_collections}")
    c2.metric("🎁 Donations", f"₹ {total_donations}")
    c3.metric("💸 Expenses", f"₹ {total_expenses}")

    c4, c5, c6 = st.columns(3)

    c4.metric("🏦 Total Loan", f"₹ {total_loans}")
    c5.metric("✅ Returned", f"₹ {returned_loans}")
    c6.metric("📌 Pending", f"₹ {pending_loans}")

    st.metric("💼 Net Balance", f"₹ {net_balance}")

    st.divider()

    st.subheader("👥 Customer Collection Report")

    if not collections_df.empty:

        customer_report = (
            collections_df.groupby("customer")["amount"]
            .sum()
            .reset_index()
        )

        st.dataframe(
            customer_report,
            use_container_width=True
        )

        st.bar_chart(
            customer_report.set_index("customer")
        )

    st.subheader("🏦 Loan Report")

    if not loans_df.empty:

        loans_df["pending"] = (
            loans_df["loan_amount"]
            - loans_df["returned"]
        )

        st.dataframe(
            loans_df,
            use_container_width=True
        )

    st.subheader("🎁 Donation Report")

    if not donations_df.empty:

        st.dataframe(
            donations_df,
            use_container_width=True
        )

    st.subheader("💸 Expense Report")

    if not expenses_df.empty:

        st.dataframe(
            expenses_df,
            use_container_width=True
        )

# =====================================================
# USER MANAGEMENT
# =====================================================

elif menu == "User Management":

    if st.session_state.role != "admin":

        st.error("Only admin allowed")

    else:

        st.title("👨‍💻 User Management")

        st.subheader("➕ Create User")

        new_username = st.text_input("New Username")

        new_password = st.text_input(
            "New Password"
        )

        new_role = st.selectbox(
            "Role",
            ["viewer", "editor", "admin"]
        )

        if st.button("Create User"):

            if new_username not in st.session_state.users:

                st.session_state.users[new_username] = {
                    "password": new_password,
                    "role": new_role,
                    "active": True
                }

                st.success("User Created")

            else:

                st.error("Username already exists")

        st.divider()

        st.subheader("👥 Existing Users")

        for user, data in st.session_state.users.items():

            st.write("---")

            c1, c2, c3 = st.columns(3)

            c1.write(f"👤 {user}")

            new_user_role = c2.selectbox(
                f"Role {user}",
                ["viewer", "editor", "admin"],
                index=["viewer", "editor", "admin"].index(
                    data["role"]
                ),
                key=f"role_{user}"
            )

            if c2.button(
                f"Update Role {user}"
            ):

                st.session_state.users[user]["role"] = new_user_role

                st.success("Role Updated")

            active_status = c3.checkbox(
                f"Active {user}",
                value=data["active"],
                key=f"active_{user}"
            )

            st.session_state.users[user]["active"] = active_status

            new_pass = st.text_input(
                f"New Password for {user}",
                key=f"pass_{user}"
            )

            if st.button(
                f"Change Password {user}"
            ):

                st.session_state.users[user]["password"] = new_pass

                st.success("Password Updated")

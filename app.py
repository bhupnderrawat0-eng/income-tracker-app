import streamlit as st
import pandas as pd
import hashlib
import datetime

st.set_page_config(page_title="Finance Pro", layout="wide")

# ================= SESSION =================
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

# ================= SIDEBAR =================
menu = st.sidebar.radio("Menu", [
    "Dashboard","Customers","Collections","Loans",
    "Donations","Expenses","Reports"
])

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.markdown("## 🚀 Bal Yuva Mangal Dal")
    st.markdown("Smart Finance Management System")

    total_col = sum(x["amount"] for x in st.session_state.collections)
    total_don = sum(x["amount"] for x in st.session_state.donations)
    total_exp = sum(x["amount"] for x in st.session_state.expenses)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("Donations", f"₹ {total_don}")
    c3.metric("Expenses", f"₹ {total_exp}")
    c4.metric("Customers", len(st.session_state.customers))

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# ================= CUSTOMERS =================
elif menu == "Customers":

    st.title("Customers")

    search = st.text_input("🔍 Search Customer")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")
    date = st.date_input("Start Date")

    if st.button("Add Customer"):
        st.session_state.customers.append({
            "name": name,
            "mobile": mobile,
            "date": str(date)
        })

    if st.session_state.customers:
        df = pd.DataFrame(st.session_state.customers)

        if search:
            df = df[df["name"].str.contains(search, case=False)]

        st.dataframe(df)

# ================= COLLECTIONS =================
elif menu == "Collections":

    st.title("Collections")

    if not st.session_state.customers:
        st.warning("Add customer first")

    else:
        cust = st.selectbox(
            "Customer",
            st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        month = st.selectbox("Month", [
            datetime.datetime.now().strftime("%B %Y")
        ])

        date = st.date_input("Collection Date")

        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            st.session_state.collections.append({
                "name": cust["name"],
                "month": month,
                "date": str(date),
                "amount": amt
            })

    if st.session_state.collections:
        df = pd.DataFrame(st.session_state.collections)

        m = st.selectbox("Filter Month", ["All"] + list(df["month"].unique()))

        if m != "All":
            df = df[df["month"] == m]

        st.dataframe(df)

        st.download_button("⬇️ Export CSV", df.to_csv().encode(), "collections.csv")

# ================= LOANS =================
elif menu == "Loans":

    st.title("Loans")

    name = st.text_input("Customer Name")
    amt = st.number_input("Loan Amount", min_value=0.0)
    date = st.date_input("Loan Start Date")

    if st.button("Add Loan"):
        st.session_state.loans.append({
            "name": name,
            "amount": amt,
            "date": str(date)
        })

    if st.session_state.loans:
        df = pd.DataFrame(st.session_state.loans)
        st.dataframe(df)

# ================= DONATIONS =================
elif menu == "Donations":

    st.title("Donations")

    name = st.text_input("Donor Name")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save Donation"):
        st.session_state.donations.append({
            "name": name,
            "amount": amt
        })

    if st.session_state.donations:
        st.dataframe(pd.DataFrame(st.session_state.donations))

# ================= EXPENSES =================
elif menu == "Expenses":

    st.title("Expenses")

    typ = st.text_input("Expense Type")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save Expense"):
        st.session_state.expenses.append({
            "type": typ,
            "amount": amt
        })

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses))

# ================= REPORTS =================
elif menu == "Reports":

    st.title("Reports")

    data = pd.DataFrame({
        "Type":["Collections","Donations","Expenses"],
        "Amount":[
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.dataframe(data)
    st.bar_chart(data.set_index("Type"))

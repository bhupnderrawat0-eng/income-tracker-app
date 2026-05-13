import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Finance Ultra Pro", layout="wide")

# ================= DARK THEME =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

h1,h2,h3,h4,h5,h6,p,label {
    color:white !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* Inputs */
input, .stSelectbox, .stNumberInput {
    background:#111827 !important;
    color:white !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border:none;
    border-radius:10px;
}

/* Cards */
[data-testid="metric-container"] {
    background: rgba(30,41,59,0.8);
    border-radius:15px;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

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

# ================= SIDEBAR =================
menu = st.sidebar.radio("Menu", [
    "Dashboard","Customers","Collections","Loans",
    "Donations","Expenses","Reports"
])

# ================= MONTH LIST FIX =================
def get_months():
    months = []
    for i in range(1,13):
        months.append(datetime.date(2026,i,1).strftime("%B %Y"))
    return months

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.markdown("## 🚀 Bal Yuva Mangal Dal")
    st.markdown("Smart Finance System")

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

    search = st.text_input("Search")

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

        # ✅ FIXED MONTH DROPDOWN
        month = st.selectbox("Month", get_months())

        date = st.date_input("Collection Date")
        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save Collection"):
            st.session_state.collections.append({
                "name": cust["name"],
                "month": month,
                "date": str(date),
                "amount": amt
            })

    if st.session_state.collections:
        df = pd.DataFrame(st.session_state.collections)

        m = st.selectbox("Filter", ["All"] + list(df["month"].unique()))

        if m != "All":
            df = df[df["month"] == m]

        st.dataframe(df)

        st.download_button("Export CSV", df.to_csv().encode(), "collections.csv")

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
        st.dataframe(pd.DataFrame(st.session_state.loans))

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

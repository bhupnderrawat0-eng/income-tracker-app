import streamlit as st
import pandas as pd
import hashlib
from streamlit_option_menu import option_menu
import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(page_title="Bal Yuva Mangal Dal", page_icon="🚀", layout="wide")

# =====================================
# CSS (FINAL FIXED UI)
# =====================================
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
div[data-testid="stToolbar"] {visibility:hidden;}
div[data-testid="stDecoration"] {visibility:hidden;}

.stApp{
    background: linear-gradient(135deg,#0f172a,#020617);
}

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#111827,#0f172a);
    border-right:1px solid rgba(255,255,255,0.08);
}

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

.stButton>button{
    border-radius:10px;
    height:45px;
    font-weight:bold;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div{
    background:#111827 !important;
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================
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

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.markdown("## 🚀 Bal Yuva Mangal Dal")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports"],
        icons=["bar-chart","people","cash","bank","gift","wallet","graph-up"],
        default_index=0
    )

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    st.title("📊 Dashboard")

    total_col = sum(x["amount"] for x in st.session_state.collections)
    total_don = sum(x["amount"] for x in st.session_state.donations)
    total_exp = sum(x["amount"] for x in st.session_state.expenses)
    balance = total_col + total_don - total_exp

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("Donations", f"₹ {total_don}")
    c3.metric("Expenses", f"₹ {total_exp}")
    c4.metric("Customers", len(st.session_state.customers))

    st.metric("Net Balance", f"₹ {balance}")

# =====================================
# CUSTOMERS
# =====================================
elif menu == "Customers":

    st.title("👥 Customers")

    col1,col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")

    with col2:
        mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        if name and mobile:
            st.session_state.customers.append({
                "name": name,
                "mobile": mobile
            })
            st.success("Added")
        else:
            st.error("Fill details")

    if st.session_state.customers:
        st.dataframe(pd.DataFrame(st.session_state.customers))

# =====================================
# COLLECTIONS
# =====================================
elif menu == "Collections":

    st.title("💰 Collections")

    if not st.session_state.customers:
        st.warning("Add customers first")

    else:
        customer = st.selectbox(
            "Customer",
            st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        month = st.selectbox(
            "Month",
            [datetime.datetime.now().strftime("%B %Y")]
        )

        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            st.session_state.collections.append({
                "name": customer["name"],
                "mobile": customer["mobile"],
                "month": month,
                "amount": amount
            })
            st.success("Saved")

    if st.session_state.collections:
        df = pd.DataFrame(st.session_state.collections)

        filter_month = st.selectbox(
            "Filter",
            ["All"] + list(df["month"].unique())
        )

        if filter_month != "All":
            df = df[df["month"] == filter_month]

        st.dataframe(df)

# =====================================
# LOANS
# =====================================
elif menu == "Loans":

    st.title("🏦 Loans")

    if not st.session_state.customers:
        st.warning("Add customers first")

    else:
        customer = st.selectbox(
            "Customer",
            st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        amount = st.number_input("Loan Amount", min_value=0.0)

        if st.button("Give Loan"):
            st.session_state.loans.append({
                "name": customer["name"],
                "amount": amount
            })
            st.success("Loan added")

    if st.session_state.loans:
        st.dataframe(pd.DataFrame(st.session_state.loans))

# =====================================
# DONATIONS
# =====================================
elif menu == "Donations":

    st.title("🎁 Donations")

    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        st.session_state.donations.append({"amount": amount})
        st.success("Saved")

# =====================================
# EXPENSES
# =====================================
elif menu == "Expenses":

    st.title("💸 Expenses")

    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        st.session_state.expenses.append({"amount": amount})
        st.success("Saved")

# =====================================
# REPORTS
# =====================================
elif menu == "Reports":

    st.title("📊 Reports")

    data = pd.DataFrame({
        "Category": ["Collections","Donations","Expenses"],
        "Amount": [
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.dataframe(data)
    st.bar_chart(data.set_index("Category"))

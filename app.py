import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(page_title="Bal Yuva Mangal Dal", page_icon="🚀", layout="wide")

# =====================================
# PREMIUM CSS (UPGRADED)
# =====================================
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
div[data-testid="stToolbar"] {visibility:hidden;}

/* BACKGROUND */
.stApp{
    background: linear-gradient(135deg,#0f172a,#020617);
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#111827,#0f172a);
    padding-top:20px;
}

/* TEXT */
h1,h2,h3,p,label{
    color:white !important;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stSelectbox div,
.stDateInput input{
    background:#111827 !important;
    color:white !important;
}

/* BUTTON */
.stButton>button{
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
    height:45px;
}

/* LOGO CARD */
.logo-card{
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:20px;
    text-align:center;
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.08);
}

/* BIG LOGO */
.logo-icon{
    font-size:60px;
    margin-bottom:10px;
}

.logo-title{
    font-size:26px;
    font-weight:bold;
    color:white;
}

.logo-sub{
    font-size:26px;
    font-weight:bold;
    color:#38bdf8;
}

.logo-tag{
    font-size:10px;
    letter-spacing:2px;
    color:#94a3b8;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================
for key in ["customers","collections","loans","donations","expenses"]:
    if key not in st.session_state:
        st.session_state[key] = []

# =====================================
# SIDEBAR (🔥 NEW LOGO)
# =====================================
with st.sidebar:

    st.markdown("""
    <div class="logo-card">
        <div class="logo-icon">🚀</div>
        <div class="logo-title">Bal Yuva</div>
        <div class="logo-sub">Mangal Dal</div>
        <div class="logo-tag">SMART FINANCE TRACKER</div>
    </div>
    """, unsafe_allow_html=True)

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

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        if name and mobile:
            st.session_state.customers.append({
                "name": name,
                "mobile": mobile
            })
            st.success("Added")

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

        start_date = st.date_input("Collection Start Date")
        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Save Collection"):
            st.session_state.collections.append({
                "name": customer["name"],
                "mobile": customer["mobile"],
                "month": month,
                "start_date": str(start_date),
                "amount": amount
            })
            st.success("Saved")

    if st.session_state.collections:
        st.dataframe(pd.DataFrame(st.session_state.collections))

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

        loan_date = st.date_input("Loan Start Date")
        amount = st.number_input("Loan Amount", min_value=0.0)

        if st.button("Give Loan"):
            st.session_state.loans.append({
                "name": customer["name"],
                "mobile": customer["mobile"],
                "start_date": str(loan_date),
                "amount": amount
            })
            st.success("Saved")

    if st.session_state.loans:
        st.dataframe(pd.DataFrame(st.session_state.loans))

# =====================================
# DONATIONS
# =====================================
elif menu == "Donations":

    st.title("🎁 Donations")

    donor = st.text_input("Donor Name")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save Donation"):
        if donor:
            st.session_state.donations.append({
                "name": donor,
                "amount": amount
            })
            st.success("Saved")

    if st.session_state.donations:
        st.dataframe(pd.DataFrame(st.session_state.donations))

# =====================================
# EXPENSES
# =====================================
elif menu == "Expenses":

    st.title("💸 Expenses")

    expense_type = st.text_input("Expense Type")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save Expense"):
        if expense_type:
            st.session_state.expenses.append({
                "type": expense_type,
                "amount": amount
            })
            st.success("Saved")

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses))

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

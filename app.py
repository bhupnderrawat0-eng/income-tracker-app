# =========================================
# SMART FINANCE TRACKER PRO
# FINAL CLEAN VERSION
# =========================================

import streamlit as st
import pandas as pd

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Smart Finance Tracker",
    layout="wide"
)

# =========================================
# SESSION STATE
# =========================================

if "collections" not in st.session_state:
    st.session_state.collections = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "customers" not in st.session_state:
    st.session_state.customers = []

if "users" not in st.session_state:
    st.session_state.users = [
        {"name": "Admin", "role": "Admin"},
        {"name": "Editor", "role": "Editor"},
        {"name": "Viewer", "role": "Viewer"}
    ]

# =========================================
# SIDEBAR DESIGN
# =========================================

st.sidebar.markdown("""
<div style="
background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.95));
padding:28px;
border-radius:24px;
margin-bottom:25px;
border:1px solid rgba(96,165,250,0.12);
box-shadow:0 8px 30px rgba(0,0,0,0.35);
text-align:center;
">

<div style="
font-size:78px;
margin-bottom:6px;
filter:drop-shadow(0 0 12px rgba(255,120,0,0.55));
">
🔥
</div>

<div style="
font-size:30px;
font-weight:800;
color:white;
line-height:1.1;
">
Bal Yuva
</div>

<div style="
font-size:30px;
font-weight:800;
color:#38bdf8;
line-height:1.1;
">
Mangal Dal
</div>

<div style="
font-size:12px;
letter-spacing:4px;
color:#94a3b8;
margin-top:12px;
font-weight:600;
">
SMART FINANCE TRACKER
</div>

</div>
""", unsafe_allow_html=True)

# =========================================
# MENU
# =========================================

menu = st.sidebar.radio(
    "",
    [
        "Dashboard",
        "Customers",
        "Collections",
        "Loans",
        "Donations",
        "Expenses",
        "Reports",
        "Users"
    ]
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#020617,#0f172a,#111827);
    color:white;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#0f172a,#1e293b);
}

div[data-baseweb="radio"] > div {
    gap: 12px;
}

div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 18px;
    margin-bottom: 12px;
    border:1px solid rgba(255,255,255,0.05);
}

div[role="radiogroup"] label:hover {
    background: rgba(59,130,246,0.18);
    transition:0.3s;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# DASHBOARD
# =========================================

if menu == "Dashboard":

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

    net_balance = (
        collections_total
        + donations_total
        - expenses_total
    )

    total_customers = len(
        st.session_state.customers
    )

    st.markdown("""
    <div style="
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.88));
    padding:28px;
    border-radius:24px;
    margin-bottom:25px;
    border:1px solid rgba(96,165,250,0.12);
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
    ">

    <div style="
    font-size:64px;
    margin-bottom:8px;
    ">
    📊 Dashboard
    </div>

    <div style="
    font-size:28px;
    font-weight:700;
    color:white;
    ">
    Welcome back 👋
    </div>

    <div style="
    font-size:18px;
    color:#94a3b8;
    margin-top:8px;
    ">
    Here's what's happening today.
    </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("💵 Collections", f"₹ {collections_total}")

    with c2:
        st.metric("🎁 Donations", f"₹ {donations_total}")

    with c3:
        st.metric("💸 Expenses", f"₹ {expenses_total}")

    with c4:
        st.metric("👥 Customers", total_customers)

    st.metric("🧾 Net Balance", f"₹ {net_balance}")

# =========================================
# CUSTOMERS
# =========================================

elif menu == "Customers":

    st.title("👥 Customers")

    customer_name = st.text_input("Customer Name")

    if st.button("Add Customer"):

        if customer_name:

            st.session_state.customers.append(
                customer_name
            )

            st.success("Customer Added")

    if st.session_state.customers:

        df = pd.DataFrame(
            st.session_state.customers,
            columns=["Customers"]
        )

        st.dataframe(df, use_container_width=True)

# =========================================
# COLLECTIONS
# =========================================

elif menu == "Collections":

    st.title("💵 Collections")

    amount = st.number_input(
        "Collection Amount",
        min_value=0
    )

    if st.button("Add Collection"):

        st.session_state.collections.append({
            "amount": amount
        })

        st.success("Collection Added")

# =========================================
# LOANS
# =========================================

elif menu == "Loans":

    st.title("🏦 Loans")

    st.info("Loan module coming soon.")

# =========================================
# DONATIONS
# =========================================

elif menu == "Donations":

    st.title("🎁 Donations")

    amount = st.number_input(
        "Donation Amount",
        min_value=0,
        key="donation"
    )

    if st.button("Add Donation"):

        st.session_state.donations.append({
            "amount": amount
        })

        st.success("Donation Added")

# =========================================
# EXPENSES
# =========================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    amount = st.number_input(
        "Expense Amount",
        min_value=0,
        key="expense"
    )

    if st.button("Add Expense"):

        st.session_state.expenses.append({
            "amount": amount
        })

        st.success("Expense Added")

# =========================================
# REPORTS
# =========================================

elif menu == "Reports":

    st.title("📈 Reports")

    report_data = {
        "Collections": [
            sum(x["amount"] for x in st.session_state.collections)
        ],
        "Donations": [
            sum(x["amount"] for x in st.session_state.donations)
        ],
        "Expenses": [
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    }

    report_df = pd.DataFrame(report_data)

    st.dataframe(report_df, use_container_width=True)

    st.bar_chart(report_df.T)

# =========================================
# USERS
# =========================================

elif menu == "Users":

    st.title("👤 User Management")

    new_user = st.text_input("User Name")

    role = st.selectbox(
        "Role",
        ["Admin", "Editor", "Viewer"]
    )

    if st.button("Add User"):

        if new_user:

            st.session_state.users.append({
                "name": new_user,
                "role": role
            })

            st.success("User Added Successfully")

    users_df = pd.DataFrame(
        st.session_state.users
    )

    st.dataframe(
        users_df,
        use_container_width=True
    )

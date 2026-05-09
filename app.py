import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Finance Tracker",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: 'Segoe UI', sans-serif !important;
}

/* MAIN BACKGROUND */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e3a8a);
    color:white;
}

/* REMOVE TOP SPACE */
.block-container{
    padding-top: 1rem !important;
    max-width: 100% !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: #111827;
    width: 320px !important;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] *{
    font-size: 22px !important;
    color: white !important;
}

/* RADIO BUTTON */
.stRadio label{
    font-size: 22px !important;
    font-weight: 600 !important;
}

/* DASHBOARD CARD */
.dashboard-card{
    background: rgba(30,41,59,0.75);
    padding: 40px;
    border-radius: 28px;
    margin-bottom: 30px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* METRIC CARD */
.metric-card{
    background: rgba(59,130,246,0.22);
    padding: 30px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

/* METRIC TITLE */
.metric-title{
    font-size: 28px !important;
    font-weight: 700 !important;
    color: white !important;
}

/* METRIC VALUE */
.metric-value{
    font-size: 52px !important;
    font-weight: 900 !important;
    color: white !important;
    margin-top: 10px;
}

/* INPUT */
input{
    font-size: 20px !important;
}

/* BUTTON */
.stButton button{
    font-size: 20px !important;
    border-radius: 15px !important;
    padding: 10px 25px !important;
}

/* HEADINGS */
h1{
    font-size: 48px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR LOGO
# =========================================================

st.sidebar.markdown("""
<div style="
background: rgba(255,255,255,0.06);
padding: 35px;
border-radius: 28px;
text-align: center;
margin-bottom: 25px;
">

<div style="
font-size: 95px;
margin-bottom: 10px;
">
🔥
</div>

<div style="
font-size: 28px;
font-weight: 800;
color: white;
line-height: 1.2;
">
Bal Yuva
</div>

<div style="
font-size: 28px;
font-weight: 800;
color: #22d3ee;
line-height: 1.2;
">
Mangal Dal
</div>

<div style="
font-size: 13px;
letter-spacing: 4px;
color: #cbd5e1;
margin-top: 14px;
">
SMART FINANCE TRACKER
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# MENU
# =========================================================

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customers",
        "Collections",
        "Donations",
        "Expenses",
        "Reports"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

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

    balance = collections_total + donations_total - expenses_total

    st.markdown("""
    <div class="dashboard-card">

    <div style="
    font-size: 68px;
    font-weight: 900;
    color: white;
    margin-bottom: 15px;
    ">
    📊 Dashboard
    </div>

    <div style="
    font-size: 40px;
    font-weight: 800;
    color: white;
    ">
    Welcome back 👋
    </div>

    <div style="
    font-size: 24px;
    color: #d1d5db;
    margin-top: 10px;
    ">
    Here's what's happening today.
    </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">💵 Collections</div>
        <div class="metric-value">₹ {collections_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">🎁 Donations</div>
        <div class="metric-value">₹ {donations_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">💸 Expenses</div>
        <div class="metric-value">₹ {expenses_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">👥 Customers</div>
        <div class="metric-value">{len(st.session_state.customers)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">🧾 Net Balance</div>
    <div class="metric-value">₹ {balance}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CUSTOMERS
# =========================================================

elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")

    if st.button("Add Customer"):

        if name != "":

            st.session_state.customers.append({
                "name": name,
                "phone": phone
            })

            st.success("Customer Added Successfully")

    if st.session_state.customers:

        df = pd.DataFrame(st.session_state.customers)
        st.dataframe(df, use_container_width=True)

# =========================================================
# COLLECTIONS
# =========================================================

elif menu == "Collections":

    st.title("💵 Collections")

    person = st.text_input("Collected From")
    amount = st.number_input("Amount", min_value=0)

    if st.button("Add Collection"):

        st.session_state.collections.append({
            "person": person,
            "amount": amount
        })

        st.success("Collection Added")

    if st.session_state.collections:

        df = pd.DataFrame(st.session_state.collections)
        st.dataframe(df, use_container_width=True)

# =========================================================
# DONATIONS
# =========================================================

elif menu == "Donations":

    st.title("🎁 Donations")

    donor = st.text_input("Donor Name")
    amount = st.number_input("Donation Amount", min_value=0)

    if st.button("Add Donation"):

        st.session_state.donations.append({
            "donor": donor,
            "amount": amount
        })

        st.success("Donation Added")

    if st.session_state.donations:

        df = pd.DataFrame(st.session_state.donations)
        st.dataframe(df, use_container_width=True)

# =========================================================
# EXPENSES
# =========================================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    item = st.text_input("Expense Title")
    amount = st.number_input("Expense Amount", min_value=0)

    if st.button("Add Expense"):

        st.session_state.expenses.append({
            "item": item,
            "amount": amount
        })

        st.success("Expense Added")

    if st.session_state.expenses:

        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True)

# =========================================================
# REPORTS
# =========================================================

elif menu == "Reports":

    st.title("📊 Reports")

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

    balance = collections_total + donations_total - expenses_total

    report_df = pd.DataFrame({
        "Category": [
            "Collections",
            "Donations",
            "Expenses",
            "Balance"
        ],
        "Amount": [
            collections_total,
            donations_total,
            expenses_total,
            balance
        ]
    })

    st.dataframe(report_df, use_container_width=True)

    st.bar_chart(
        report_df.set_index("Category")
    )

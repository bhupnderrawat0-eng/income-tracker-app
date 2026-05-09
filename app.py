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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:'Segoe UI',sans-serif;
}

.stApp{
    background:
    radial-gradient(circle at top left,#1e3a8a 0%,#020617 40%),
    linear-gradient(to bottom right,#0f172a,#111827);
    color:white;
}

section[data-testid="stSidebar"]{
    background:rgba(15,23,42,0.92);
    border-right:1px solid rgba(255,255,255,0.08);
}

.block-container{
    padding-top:2rem;
}

.metric-card{
    background:rgba(30,41,59,0.75);
    padding:24px;
    border-radius:22px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
}

.metric-title{
    color:#ffffff;
    font-size:20px;
    font-weight:700;
    margin-bottom:12px;
}

.metric-value{
    color:#ffffff;
    font-size:46px;
    font-weight:900;
}

.menu-title{
    font-size:14px;
    letter-spacing:4px;
    color:#cbd5e1;
    margin-top:12px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR LOGO
# =========================================================

st.sidebar.markdown("""
<div style="
background: rgba(255,255,255,0.05);
padding: 25px;
border-radius: 24px;
text-align: center;
margin-bottom: 20px;
">

<div style="
font-size: 72px;
margin-bottom: 8px;
">
🔥
</div>

<div style="
font-size: 22px;
font-weight: 800;
color: white;
line-height: 1.2;
">
Bal Yuva
</div>

<div style="
font-size: 22px;
font-weight: 800;
color: #38bdf8;
line-height: 1.2;
">
Mangal Dal
</div>

<div style="
font-size: 11px;
letter-spacing: 3px;
color: #cbd5e1;
margin-top: 10px;
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
    <div style="
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.88));
    padding:28px;
    border-radius:24px;
    margin-bottom:25px;
    border:1px solid rgba(96,165,250,0.12);
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
    ">

    <div style="
    font-size:58px;
    font-weight:800;
    color:white;
    margin-bottom:10px;
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

    st.title("📈 Reports")

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

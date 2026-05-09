import streamlit as st
import pandas as pd

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Smart Finance Tracker",
    page_icon="🔥",
    layout="wide"
)

# =========================================
# SESSION STATE
# =========================================
if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "users" not in st.session_state:
    st.session_state.users = [
        {"name": "Admin", "role": "Admin"},
        {"name": "Editor", "role": "Editor"},
        {"name": "Viewer", "role": "Viewer"}
    ]

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: #050816;
    color: white;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.15), transparent 25%),
        radial-gradient(circle at bottom right, rgba(139,92,246,0.12), transparent 25%),
        #050816;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: rgba(10,15,30,0.92);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 18px;
    border: none;
    padding: 14px;
    background: linear-gradient(135deg,#243b55,#141e30);
    color: white;
    font-weight: 700;
    font-size: 17px;
    margin-bottom: 12px;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(135deg,#3b82f6,#8b5cf6);
}

/* Cards */

.metric-card {
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

.metric-title {
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 42px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR LOGO
# =========================================
with st.sidebar:

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.88));
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
            font-size:14px;
            letter-spacing:4px;
            color:#cbd5e1;
            margin-top:12px;
        ">
            SMART FINANCE TRACKER
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# MENU
# =========================================
menu = st.sidebar.radio(
    "Navigation",
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

# =========================================
# CUSTOMERS
# =========================================
elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input("Customer Name")

    if st.button("Add Customer"):
        if name:
            st.session_state.customers.append(name)
            st.success("Customer Added")

    st.write(st.session_state.customers)

# =========================================
# COLLECTIONS
# =========================================
elif menu == "Collections":

    st.title("💵 Collections")

    cname = st.text_input("Customer Name")
    amount = st.number_input("Amount", step=100)

    if st.button("Add Collection"):
        st.session_state.collections.append({
            "name": cname,
            "amount": amount
        })
        st.success("Collection Added")

    st.dataframe(pd.DataFrame(st.session_state.collections))

# =========================================
# LOANS
# =========================================
elif menu == "Loans":

    st.title("🏦 Loans")

    st.info("Loan module ready for next upgrade.")

# =========================================
# DONATIONS
# =========================================
elif menu == "Donations":

    st.title("🎁 Donations")

    donor = st.text_input("Donor Name")
    amount = st.number_input("Donation Amount", step=100)

    if st.button("Add Donation"):
        st.session_state.donations.append({
            "name": donor,
            "amount": amount
        })
        st.success("Donation Added")

    st.dataframe(pd.DataFrame(st.session_state.donations))

# =========================================
# EXPENSES
# =========================================
elif menu == "Expenses":

    st.title("💸 Expenses")

    item = st.text_input("Expense Name")
    amount = st.number_input("Expense Amount", step=100)

    if st.button("Add Expense"):
        st.session_state.expenses.append({
            "item": item,
            "amount": amount
        })
        st.success("Expense Added")

    st.dataframe(pd.DataFrame(st.session_state.expenses))

# =========================================
# REPORTS
# =========================================
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

    report_df = pd.DataFrame({
        "Category": [
            "Collections",
            "Donations",
            "Expenses"
        ],
        "Amount": [
            collections_total,
            donations_total,
            expenses_total
        ]
    })

    st.dataframe(report_df)

    st.bar_chart(report_df.set_index("Category"))

# =========================================
# USERS
# =========================================
elif menu == "Users":

    st.title("👤 User Management")

    new_user = st.text_input("User Name")

    role = st.selectbox(
        "Role",
        [
            "Admin",
            "Editor",
            "Viewer"
        ]
    )

    if st.button("Add User"):

        if new_user:

            st.session_state.users.append({
                "name": new_user,
                "role": role
            })

            st.success("User Added Successfully")

    st.write("")

    st.subheader("Current Users")

    users_df = pd.DataFrame(
        st.session_state.users
    )

    st.dataframe(
        users_df,
        use_container_width=True
    )

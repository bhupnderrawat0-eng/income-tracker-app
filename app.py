import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bal Yuva Mangal Dal",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM DARK UI
# =====================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
    color:white;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617,
        #0f172a
    );
    border-right:
    1px solid rgba(255,255,255,0.08);
}

/* Metric Cards */

div[data-testid="metric-container"] {

    background:
    rgba(17,24,39,0.85);

    border:
    1px solid rgba(255,255,255,0.08);

    padding:22px;

    border-radius:20px;

    backdrop-filter:blur(12px);

    box-shadow:
    0 8px 30px rgba(0,0,0,0.35);

    transition:0.3s;
}

div[data-testid="metric-container"]:hover {

    transform:translateY(-4px);

    box-shadow:
    0 12px 35px rgba(0,0,0,0.45);
}

div[data-testid="metric-container"] label {
    color:#94a3b8 !important;
}

div[data-testid="metric-container"] div {
    color:white !important;
}

/* Buttons */

.stButton>button {

    width:100%;
    border-radius:14px;
    height:3.2em;
    border:none;
    font-weight:600;
    color:white;

    background:
    linear-gradient(
    90deg,
    #2563eb,
    #1d4ed8
    );
}

/* Inputs */

.stTextInput>div>div>input,
.stNumberInput>div>div>input {

    border-radius:12px;
}

/* Tables */

[data-testid="stDataFrame"] {
    border-radius:16px;
    overflow:hidden;
}

h1,h2,h3 {
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

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
# LOGIN FUNCTION
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

    st.title("🔐 Bal Yuva Mangal Dal Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        success = login(
            username,
            password
        )

        if success:

            st.success("Login Successful")
            st.rerun()

        else:

            st.error("Invalid Login")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "logo.png",
        width=220
    )

    st.markdown("""

    <h2 style='
    text-align:center;
    color:white;
    margin-top:-10px;
    '>

    Bal Yuva Mangal Dal

    </h2>

    <p style='
    text-align:center;
    color:#94a3b8;
    font-size:14px;
    margin-top:-15px;
    '>

    SMART FINANCE TRACKER

    </p>

    """, unsafe_allow_html=True)

    menu = option_menu(
        menu_title=None,

        options=[
            "Dashboard",
            "Customers",
            "Collections",
            "Loans",
            "Donations",
            "Expenses",
            "Reports",
            "Users"
        ],

        icons=[
            "house-fill",
            "people-fill",
            "cash-stack",
            "bank2",
            "gift-fill",
            "wallet2",
            "bar-chart-fill",
            "person-fill"
        ],

        default_index=0
    )

    st.divider()

    st.write(f"👤 {st.session_state.username}")
    st.write(f"🔐 {st.session_state.role}")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.rerun()

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.title("📊 Dashboard")

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

    remaining_loans = (
        total_loans
        - returned_loans
    )

    balance = (
        collections_total
        + donations_total
        - expenses_total
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💵 Collections",
        f"₹ {collections_total:,.0f}"
    )

    c2.metric(
        "🎁 Donations",
        f"₹ {donations_total:,.0f}"
    )

    c3.metric(
        "💸 Expenses",
        f"₹ {expenses_total:,.0f}"
    )

    c4.metric(
        "🏦 Loan Pending",
        f"₹ {remaining_loans:,.0f}"
    )

    st.write("")

    c5, c6 = st.columns(2)

    c5.metric(
        "🪙 Net Balance",
        f"₹ {balance:,.0f}"
    )

    c6.metric(
        "👥 Customers",
        len(st.session_state.customers)
    )

    st.divider()

    chart_data = pd.DataFrame({

        "Category":[
            "Collections",
            "Donations",
            "Expenses"
        ],

        "Amount":[
            collections_total,
            donations_total,
            expenses_total
        ]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Amount",
        text="Amount",
        title="Finance Overview"
    )

    fig.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# CUSTOMERS
# =====================================================

elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input(
        "Customer Name"
    )

    if st.button("Add Customer"):

        if name != "":

            st.session_state.customers.append(name)

            st.success("Customer Added")

    if st.session_state.customers:

        df = pd.DataFrame(
            st.session_state.customers,
            columns=["Customer Name"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

# =====================================================
# COLLECTIONS
# =====================================================

elif menu == "Collections":

    st.title("💵 Collections")

    if len(st.session_state.customers) == 0:

        st.warning(
            "Please add customers first"
        )

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

        if st.button("Save Collection"):

            st.session_state.collections.append({
                "customer": customer,
                "month": month,
                "amount": amount,
                "status": status
            })

            st.success("Collection Saved")

# =====================================================
# LOANS
# =====================================================

elif menu == "Loans":

    st.title("🏦 Loans")

    customer = st.selectbox(
        "Customer",
        st.session_state.customers
        if st.session_state.customers
        else ["No Customers"]
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0
    )

    interest = st.number_input(
        "Interest %",
        min_value=0.0
    )

    if st.button("Start Loan"):

        st.session_state.loans.append({

            "customer": customer,
            "loan_amount": loan_amount,
            "returned": 0.0,
            "interest_rate": interest
        })

        st.success("Loan Started")

# =====================================================
# DONATIONS
# =====================================================

elif menu == "Donations":

    st.title("🎁 Donations")

    donor_name = st.text_input(
        "Donor Name"
    )

    donation_amount = st.number_input(
        "Donation Amount",
        min_value=0.0
    )

    if st.button("Save Donation"):

        st.session_state.donations.append({

            "name": donor_name,
            "amount": donation_amount
        })

        st.success("Donation Saved")

# =====================================================
# EXPENSES
# =====================================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    expense_title = st.text_input(
        "Expense Title"
    )

    expense_amount = st.number_input(
        "Expense Amount",
        min_value=0.0
    )

    if st.button("Save Expense"):

        st.session_state.expenses.append({

            "title": expense_title,
            "amount": expense_amount
        })

        st.success("Expense Saved")

# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":

    st.title("📊 Reports")

    collections_df = pd.DataFrame(
        st.session_state.collections
    )

    if not collections_df.empty:

        st.dataframe(
            collections_df,
            use_container_width=True
        )

# =====================================================
# USERS
# =====================================================

elif menu == "Users":

    if st.session_state.role != "admin":

        st.error("Only admin allowed")

    else:

        st.title("👨‍💻 User Management")

        new_username = st.text_input(
            "New Username"
        )

        new_password = st.text_input(
            "New Password"
        )

        new_role = st.selectbox(
            "Role",
            ["viewer", "editor", "admin"]
        )

        if st.button("Create User"):

            st.session_state.users[new_username] = {

                "password": new_password,
                "role": new_role,
                "active": True
            }

            st.success("User Created")

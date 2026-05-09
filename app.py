import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
import base64

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
# PREMIUM CSS
# =====================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:1rem;
    padding-bottom:0rem !important;
}

/* MAIN APP */

.stApp {
    background:
    radial-gradient(circle at top,
    #0f172a,
    #020617);
    color:white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
    linear-gradient(
    180deg,
    #020617,
    #0f172a
    );

    border-right:
    1px solid rgba(255,255,255,0.08);

    min-height:100vh;
    overflow-y:auto;
}

/* OPTION MENU FIX */

.st-emotion-cache-1v0mbdj{
    background:transparent !important;
}

ul[data-testid="stSidebarNavItems"]{
    background:transparent !important;
}

/* METRIC CARDS */

div[data-testid="metric-container"] {

    background:
    rgba(15,23,42,0.75);

    border:
    1px solid rgba(255,255,255,0.06);

    border-radius:22px;

    padding:20px;

    backdrop-filter:blur(12px);

    box-shadow:
    0 8px 30px rgba(0,0,0,0.4);

    transition:0.3s;
}

div[data-testid="metric-container"]:hover {
    transform:translateY(-4px);
}

/* BUTTON */

.stButton>button {

    width:100%;
    height:48px;

    border:none;

    border-radius:14px;

    font-size:16px;

    font-weight:600;

    color:white;

    background:
    linear-gradient(
    90deg,
    #2563eb,
    #4f46e5
    );
}

h1,h2,h3,h4 {
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
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

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

with st.sidebar:

    st.markdown("""
    <div style="
    height:95px;
    overflow:hidden;
    display:flex;
    justify-content:center;
    align-items:center;
    margin-bottom:0px;
    ">

    <img src="data:image/png;base64,{}"
    width="120"
    style="
    object-fit:contain;
    transform:scale(1.85);
    mix-blend-mode:screen;
    filter:brightness(1.15);
    "/>

    </div>
    """.format(
        base64.b64encode(
            open("logo.png", "rb").read()
        ).decode()
    ), unsafe_allow_html=True)

    st.markdown("""
    <h2 style='
    text-align:center;
    color:white;
    font-size:20px;
    font-weight:800;
    margin-top:5px;
    margin-bottom:0px;
    '>
    Bal Yuva Mangal Dal
    </h2>

    <p style='
    text-align:center;
    color:#cbd5e1;
    font-size:12px;
    margin-bottom:8px;
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

        default_index=0,

        styles={

            "container": {
                "padding":"0!important",
                "background-color":"transparent!important",
            },

            "icon": {
                "color":"white",
                "font-size":"17px"
            },

            "nav-link": {

                "font-size":"15px",
                "text-align":"left",
                "margin":"2px",
                "border-radius":"12px",
                "color":"#ffffff",
                "padding":"8px",
                "--hover-color":"#1e293b",
            },

            "nav-link-selected": {

                "background":
                "linear-gradient(90deg,#2563eb,#4f46e5)",
            },
        }
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

    st.markdown("""
    # 📊 Dashboard

    ### Welcome back 👋
    Here's what's happening today.
    """)

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
        f"₹ {collections_total}"
    )

    c2.metric(
        "🎁 Donations",
        f"₹ {donations_total}"
    )

    c3.metric(
        "💸 Expenses",
        f"₹ {expenses_total}"
    )

    c4.metric(
        "🏦 Loan Pending",
        f"₹ {remaining_loans}"
    )

    st.write("")

    c5, c6 = st.columns(2)

    c5.metric(
        "🪙 Net Balance",
        f"₹ {balance}"
    )

    c6.metric(
        "👥 Customers",
        len(st.session_state.customers)
    )

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
# COLLECTIONS
# =====================================================

elif menu == "Collections":

    st.title("💵 Collections")

    if len(st.session_state.customers) == 0:

        st.warning("Please add customers first")

    else:

        customer = st.selectbox(
            "Customer",
            st.session_state.customers
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        if st.button("Save Collection"):

            st.session_state.collections.append({
                "customer": customer,
                "amount": amount
            })

            st.success("Collection Saved")

# =====================================================
# LOANS
# =====================================================

elif menu == "Loans":

    st.title("🏦 Loans")

    st.write("Loan section ready.")

# =====================================================
# DONATIONS
# =====================================================

elif menu == "Donations":

    st.title("🎁 Donations")

    st.write("Donation section ready.")

# =====================================================
# EXPENSES
# =====================================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    st.write("Expense section ready.")

# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":

    st.title("📊 Reports")

    st.write("Reports section ready.")

# =====================================================
# USERS
# =====================================================

elif menu == "Users":

    st.title("👨‍💻 User Management")

    users_df = pd.DataFrame(
        st.session_state.users
    ).T

    st.dataframe(
        users_df,
        use_container_width=True
    )NFIG
# =====================================================

st.set_page_config(
    page_title="Bal Yuva Mangal Dal",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM CSS
# =====================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:1rem;
    padding-bottom:0rem !important;
}

/* MAIN APP */

.stApp {

    background:
    radial-gradient(circle at top,
    #0f172a,
    #020617);

    color:white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #020617,
    #0f172a
    );

    border-right:
    1px solid rgba(255,255,255,0.08);

    min-height:100vh;
    overflow-y:auto;
}

/* METRIC CARDS */

div[data-testid="metric-container"] {

    background:
    rgba(15,23,42,0.75);

    border:
    1px solid rgba(255,255,255,0.06);

    border-radius:22px;

    padding:20px;

    backdrop-filter:blur(12px);

    box-shadow:
    0 8px 30px rgba(0,0,0,0.4);

    transition:0.3s;
}

div[data-testid="metric-container"]:hover {

    transform:translateY(-4px);
}

/* BUTTON */

.stButton>button {

    width:100%;
    height:48px;

    border:none;

    border-radius:14px;

    font-size:16px;

    font-weight:600;

    color:white;

    background:
    linear-gradient(
    90deg,
    #2563eb,
    #4f46e5
    );
}

h1,h2,h3,h4 {
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
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

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

with st.sidebar:

    st.markdown("""
    <div style="
    height:70px;
    overflow:hidden;
    display:flex;
    justify-content:center;
    align-items:center;
    margin-bottom:0px;
    ">

    <img src="data:image/png;base64,{}"
    width="120"
    style="
    object-fit:contain;
    transform:scale(2.1);
    mix-blend-mode:screen;
    filter:brightness(1.15);
    "/>

    </div>
    """.format(
        base64.b64encode(
            open("logo.png", "rb").read()
        ).decode()
    ), unsafe_allow_html=True)

    st.markdown("""
    <h2 style='
    text-align:center;
    color:white;
    font-size:20px;
    font-weight:800;
    margin-top:5px;
    margin-bottom:0px;
    '>
    Bal Yuva Mangal Dal
    </h2>

    <p style='
    text-align:center;
    color:#cbd5e1;
    font-size:12px;
    margin-bottom:8px;
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

        default_index=0,

        styles={

            "container": {
                "padding":"0px",
                "background-color":"transparent",
            },

            "icon": {
                "color":"white",
                "font-size":"17px"
            },

            "nav-link": {

                "font-size":"15px",
                "text-align":"left",
                "margin":"2px",
                "border-radius":"12px",
                "color":"#ffffff",
                "padding":"8px",
                "--hover-color":"#1e293b",
            },

            "nav-link-selected": {

                "background":
                "linear-gradient(90deg,#2563eb,#4f46e5)",
            },
        }
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

    st.markdown("""
    # 📊 Dashboard

    ### Welcome back 👋
    Here's what's happening today.
    """)

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
        f"₹ {collections_total}"
    )

    c2.metric(
        "🎁 Donations",
        f"₹ {donations_total}"
    )

    c3.metric(
        "💸 Expenses",
        f"₹ {expenses_total}"
    )

    c4.metric(
        "🏦 Loan Pending",
        f"₹ {remaining_loans}"
    )

    st.write("")

    c5, c6 = st.columns(2)

    c5.metric(
        "🪙 Net Balance",
        f"₹ {balance}"
    )

    c6.metric(
        "👥 Customers",
        len(st.session_state.customers)
    )

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
# COLLECTIONS
# =====================================================

elif menu == "Collections":

    st.title("💵 Collections")

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

    donor_name = st.text_input("Donor Name")

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

    expense_title = st.text_input("Expense Title")

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

    if st.session_state.collections:

        st.dataframe(
            pd.DataFrame(st.session_state.collections),
            use_container_width=True
        )

# =====================================================
# USERS
# =====================================================

elif menu == "Users":

    st.title("👨‍💻 User Management")

    users_df = pd.DataFrame(
        st.session_state.users
    ).T

    st.dataframe(
        users_df,
        use_container_width=True
    )

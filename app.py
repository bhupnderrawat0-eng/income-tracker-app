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

#MainMenu {
    visibility:hidden;
}

footer {
    visibility:hidden;
}

header {
    visibility:hidden;
}

.stApp {
    background:
    linear-gradient(
    135deg,
    #020617,
    #0f172a,
    #111827
    );
    color:white;
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #020617,
    #0f172a
    );

    border-right:
    1px solid rgba(255,255,255,0.08);
}

/* =========================
METRIC CARDS
========================= */

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

/* =========================
BUTTONS
========================= */

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

    transition:0.3s;
}

.stButton>button:hover {

    transform:scale(1.02);

    background:
    linear-gradient(
    90deg,
    #1d4ed8,
    #2563eb
    );
}

/* =========================
INPUTS
========================= */

.stTextInput>div>div>input,
.stNumberInput>div>div>input {

    border-radius:12px;
}

/* =========================
TABLES
========================= */

[data-testid="stDataFrame"] {

    border-radius:16px;
    overflow:hidden;
}

/* =========================
HEADINGS
========================= */

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
# PREMIUM SIDEBAR
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

        default_index=0,

        styles={

            "container": {
                "padding":"0!important",
                "background-color":"transparent"
            },

            "icon": {
                "color":"white",
                "font-size":"18px"
            },

            "nav-link": {

                "font-size":"16px",
                "text-align":"left",
                "margin":"6px",
                "border-radius":"14px",
                "color":"#e2e8f0",
                "padding":"12px",
            },

            "nav-link-selected": {

                "background":
                "linear-gradient(90deg,#2563eb,#1d4ed8)",

                "color":"white",
            },
        }
    )

    st.divider()

    st.markdown(f"""

    <div style="
    background:rgba(17,24,39,0.9);
    padding:15px;
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.08);
    ">

    <h4 style="color:white;">
    👤 {st.session_state.username}
    </h4>

    <p style="color:#94a3b8;">
    🔐 {st.session_state.role}
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.write("")

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

    # =========================
    # METRICS
    # =========================

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

    # =========================
    # CHART
    # =========================

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

        font_color="white",

        title_font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =========================
    # QUICK ACTIONS
    # =========================

    st.subheader("⚡ Quick Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.button("➕ Add Customer")

    with q2:
        st.button("💰 Add Collection")

    with q3:
        st.button("🏦 Start Loan")

    with q4:
        st.button("🎁 Add Donation")

    st.divider()

    # =========================
    # FOOTER
    # =========================

    st.markdown("""

    <div style="
    text-align:center;
    color:#94a3b8;
    padding:20px;
    ">

    Made with ❤️ by
    <span style="color:#fbbf24;">
    Bal Yuva Mangal Dal
    </span>

    </div>

    """, unsafe_allow_html=True)

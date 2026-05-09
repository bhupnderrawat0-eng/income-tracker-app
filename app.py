import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bal Yuva Mangal Dal",
    page_icon="🪔",
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

    width:320px !important;
    min-width:320px !important;

    background:
    linear-gradient(
    180deg,
    #020617,
    #0f172a
    );

    background-color:#020617 !important;

    border-right:
    1px solid rgba(255,255,255,0.08);

    min-height:100vh;
}

/* FIX WHITE BACKGROUND */

.st-emotion-cache-1v0mbdj,
.st-emotion-cache-16txtl3,
.st-emotion-cache-6qob1r,
.css-1d391kg,
.css-163ttbj,
.css-1wrcr25 {
    background: transparent !important;
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

h1,h2,h3,h4,h5,p {
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="
    text-align:center;
    padding-top:10px;
    padding-bottom:20px;
    ">

    <div style="
    font-size:60px;
    ">
    🪔
    </div>

    <h1 style="
    color:#facc15;
    font-size:26px;
    margin-top:-10px;
    font-weight:800;
    ">
    Bal Yuva
    </h1>

    <h2 style="
    color:white;
    font-size:22px;
    margin-top:-18px;
    font-weight:700;
    ">
    Mangal Dal
    </h2>

    <p style="
    color:#cbd5e1;
    font-size:12px;
    letter-spacing:2px;
    margin-top:-5px;
    ">
    SMART FINANCE TRACKER
    </p>

    </div>
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
                "background-color":"transparent",
            },

            "icon": {
                "color":"#ffffff",
                "font-size":"18px"
            },

            "nav-link": {

                "font-size":"15px",

                "text-align":"left",

                "margin":"6px 0px",

                "border-radius":"14px",

                "color":"#e2e8f0",

                "padding":"12px 16px",

                "background-color":"transparent",

                "transition":"0.3s",
            },

            "nav-link-selected": {

                "background":
                "linear-gradient(90deg,#2563eb,#4f46e5)",

                "color":"white",

                "font-weight":"700",

                "box-shadow":
                "0 4px 15px rgba(37,99,235,0.4)",
            },
        }
    )

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
        "👥 Customers",
        len(st.session_state.customers)
    )

    st.write("")

    st.metric(
        "🪙 Net Balance",
        f"₹ {balance}"
    )

# =====================================================
# CUSTOMERS
# =====================================================

elif menu == "Customers":

    st.title("👥 Customers")

    name = st.text_input("Customer Name")

    if st.button("Add Customer"):

        if name:
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

        st.warning("Add customers first")

    else:

        customer = st.selectbox(
            "Select Customer",
            st.session_state.customers
        )

        amount = st.number_input(
            "Collection Amount",
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
    st.info("Loans section ready")

# =====================================================
# DONATIONS
# =====================================================

elif menu == "Donations":

    st.title("🎁 Donations")

    amount = st.number_input(
        "Donation Amount",
        min_value=0.0
    )

    if st.button("Save Donation"):

        st.session_state.donations.append({
            "amount": amount
        })

        st.success("Donation Saved")

# =====================================================
# EXPENSES
# =====================================================

elif menu == "Expenses":

    st.title("💸 Expenses")

    amount = st.number_input(
        "Expense Amount",
        min_value=0.0
    )

    if st.button("Save Expense"):

        st.session_state.expenses.append({
            "amount": amount
        })

        st.success("Expense Saved")

# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":

    st.title("📊 Reports")

    report_data = pd.DataFrame({

        "Category": [
            "Collections",
            "Donations",
            "Expenses"
        ],

        "Amount": [

            sum(x["amount"] for x in st.session_state.collections),

            sum(x["amount"] for x in st.session_state.donations),

            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.dataframe(
        report_data,
        use_container_width=True
    )

    st.bar_chart(
        report_data.set_index("Category")
    )

# =====================================================
# USERS
# =====================================================

elif menu == "Users":

    st.title("👨‍💻 Users")

    st.info("Admin Panel Ready")

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bal Yuva Mangal Dal",
    page_icon="🚀",
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

/* APP BACKGROUND */

.stApp{
    background:
    linear-gradient(
    135deg,
    #0f172a,
    #020617
    );
}

/* MAIN CONTENT */

.block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{

    background:
    linear-gradient(
    180deg,
    #111827,
    #0f172a
    );

    border-right:
    1px solid rgba(255,255,255,0.08);

    width:320px !important;
}

/* TEXT */

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

/* METRIC CARDS */

div[data-testid="metric-container"]{

    background:
    linear-gradient(
    135deg,
    rgba(30,41,59,0.95),
    rgba(15,23,42,0.95)
    );

    border:
    1px solid rgba(96,165,250,0.15);

    border-radius:22px;

    padding:28px;

    box-shadow:
    0 10px 35px rgba(0,0,0,0.45);

    backdrop-filter:blur(14px);
}

/* BUTTONS */

.stButton>button{

    width:100%;

    border:none;

    border-radius:12px;

    height:48px;

    font-size:16px;

    font-weight:700;

    color:white;

    background:
    linear-gradient(
    90deg,
    #2563eb,
    #7c3aed
    );
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stSelectbox div{

    background:#111827 !important;

    color:white !important;

    border-radius:10px !important;
}

/* DATAFRAME */

[data-testid="stDataFrame"]{
    border-radius:15px;
    overflow:hidden;
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

if "users" not in st.session_state:

    st.session_state.users = [

        {
            "name":"Admin",
            "role":"Admin"
        }
    ]

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style='
    background:rgba(255,255,255,0.04);
    padding:22px;
    border-radius:22px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.06);
    margin-bottom:20px;
    '>

    <div style='
font-size:78px;
margin-bottom:6px;
filter:drop-shadow(0 0 12px rgba(255,120,0,0.55));
'>
🔥
</div>

    <div style='
    font-size:30px;
    font-weight:800;
    color:white;
    line-height:1.1;
    '>
    Bal Yuva
    </div>

    <div style='
    font-size:30px;
    font-weight:800;
    color:#38bdf8;
    line-height:1.1;
    margin-bottom:10px;
    '>
    Mangal Dal
    </div>

    <div style='
    font-size:11px;
    letter-spacing:3px;
    color:#94a3b8;
    '>
    SMART FINANCE TRACKER
    </div>

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
            "grid-fill",
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

            "container":{
                "background-color":"transparent",
                "padding":"0px"
            },

            "icon":{
                "color":"white",
                "font-size":"18px"
            },

            "nav-link":{

                "font-size":"16px",

                "text-align":"left",

                "margin":"8px 0",

                "padding":"14px",

                "border-radius":"14px",

                "background-color":"#1e293b",

                "color":"white",

                "--hover-color":"#334155",
            },

            "nav-link-selected":{

                "background":
                "linear-gradient(90deg,#2563eb,#7c3aed)",

                "font-weight":"700",
            }
        }
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.markdown("""
    <div style='

    background:
    linear-gradient(
    135deg,
    rgba(15,23,42,0.88),
    rgba(30,41,59,0.88)
    );

    padding:28px;

    border-radius:24px;

    margin-bottom:25px;

    border:1px solid rgba(96,165,250,0.12);

    box-shadow:0 8px 30px rgba(0,0,0,0.35);

    '>

    <div style='
    font-size:52px;
    font-weight:800;
    color:white;
    '>
    📊 Dashboard
    </div>

    <div style='
    font-size:34px;
    font-weight:700;
    margin-top:10px;
    color:white;
    '>
    Welcome back 👋
    </div>

    <div style='
    font-size:18px;
    color:#94a3b8;
    margin-top:8px;
    '>
    Here's what's happening today.
    </div>

    </div>
    """, unsafe_allow_html=True)

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

    with c1:
        st.metric(
            "💵 Collections",
            f"₹ {collections_total}"
        )

    with c2:
        st.metric(
            "🎁 Donations",
            f"₹ {donations_total}"
        )

    with c3:
        st.metric(
            "💸 Expenses",
            f"₹ {expenses_total}"
        )

    with c4:
        st.metric(
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

            st.success("Customer Added Successfully")

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

            st.success("Collection Saved Successfully")

# =====================================================
# LOANS
# =====================================================

elif menu == "Loans":

    st.title("🏦 Loans")

    st.info("Loans Section Ready")

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

        st.success("Donation Saved Successfully")

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

        st.success("Expense Saved Successfully")

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

            sum(
                x["amount"]
                for x in st.session_state.collections
            ),

            sum(
                x["amount"]
                for x in st.session_state.donations
            ),

            sum(
                x["amount"]
                for x in st.session_state.expenses
            )
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

    st.title("👨‍💻 User Management")

    col1, col2 = st.columns(2)

    with col1:

        username = st.text_input("User Name")

    with col2:

        role = st.selectbox(
            "Select Role",
            ["Admin", "Editor", "Viewer"]
        )

    if st.button("Add User"):

        if username:

            st.session_state.users.append({

                "name": username,
                "role": role
            })

            st.success("User Added Successfully")

    st.write("")

    users_df = pd.DataFrame(
        st.session_state.users
    )

    st.dataframe(
        users_df,
        use_container_width=True
    )

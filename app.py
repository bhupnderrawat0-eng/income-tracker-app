import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva SaaS", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#020617,#0f172a);}
header, footer {visibility:hidden;}

.block-container {padding-top:1rem;}

h1,h2,h3,h4,h5,p,label {color:white !important;}

section[data-testid="stSidebar"] {background:#020617;}

.stTextInput input, .stNumberInput input, .stSelectbox div {
    background:#111827 !important;
    color:white !important;
}

.stButton>button {
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
}

/* HEADER */
.header {
    background: rgba(30,41,59,0.6);
    padding:20px;
    border-radius:20px;
    margin-bottom:25px;
}

/* SECTION BOX */
.box {
    background: rgba(30,41,59,0.6);
    padding:20px;
    border-radius:15px;
    margin-top:15px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
for key in ["customers","collections","loans","donations","expenses"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "users" not in st.session_state:
    st.session_state.users = [{
        "username":"admin",
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role":"Admin"
    }]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hashlib.sha256(p.encode()).hexdigest()

        for user in st.session_state.users:
            if user["username"] == u and user["password"] == hashed:
                st.session_state.logged_in = True
                st.session_state.current_user = u
                st.session_state.role = user["role"]
                st.rerun()

        st.error("Invalid Login")

    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🚀 Bal Yuva SaaS")

    menu = option_menu(
        None,
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"]
    )

    st.write("---")
    st.write(st.session_state.current_user)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================= HEADER =================
st.markdown("""
    <div style="
        background: rgba(0,0,0,0.4);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    ">
        <h2 style='color:white;'>🚀 Bal Yuva Mangal Dal</h2>
        <p style='color:lightgray;'>Smart Finance SaaS System</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# ================= DASHBOARD =================
if menu == "Dashboard":

    c1,c2,c3,c4 = st.columns(4)

    total_col = sum(x["amount"] for x in st.session_state.collections)
    total_loan = sum(x["amount"] for x in st.session_state.loans)
    total_don = sum(x["amount"] for x in st.session_state.donations)
    total_exp = sum(x["amount"] for x in st.session_state.expenses)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("Loans", f"₹ {total_loan}")
    c3.metric("Donations", f"₹ {total_don}")
    c4.metric("Expenses", f"₹ {total_exp}")

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# ================= CUSTOMERS =================
elif menu == "Customers":

    st.subheader("Add Customer")

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        st.session_state.customers.append({"name":name,"mobile":mobile})

    st.markdown("### Customer List")
    st.dataframe(pd.DataFrame(st.session_state.customers))

# ================= COLLECTION =================
elif menu == "Collections":

    if st.session_state.customers:

        cust = st.selectbox("Customer", st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})")

        month = st.selectbox("Month",
            [datetime.date(2026,m,1).strftime("%B %Y") for m in range(1,13)]
        )

        date = st.date_input("Start Date")
        amt = st.number_input("Amount")

        if st.button("Save Collection"):
            st.session_state.collections.append({
                "name":cust["name"],
                "month":month,
                "date":str(date),
                "amount":amt
            })

    st.markdown("### Records")
    st.dataframe(pd.DataFrame(st.session_state.collections))

# ================= LOANS =================
elif menu == "Loans":

    if st.session_state.customers:

        cust = st.selectbox("Customer", st.session_state.customers,
            format_func=lambda x: x["name"])

        date = st.date_input("Loan Start Date")
        amt = st.number_input("Amount")

        if st.button("Add Loan"):
            st.session_state.loans.append({
                "name":cust["name"],
                "date":str(date),
                "amount":amt
            })

    st.markdown("### Loan Records")
    st.dataframe(pd.DataFrame(st.session_state.loans))

# ================= DONATIONS FIX =================
elif menu == "Donations":

    st.subheader("Add Donation")

    donor = st.text_input("Donor Name")
    amt = st.number_input("Amount")

    if st.button("Save Donation"):
        st.session_state.donations.append({
            "name": donor,
            "amount": amt
        })

    st.markdown("### Donation Records")
    st.dataframe(pd.DataFrame(st.session_state.donations))

# ================= EXPENSE FIX =================
elif menu == "Expenses":

    st.subheader("Add Expense")

    exp_type = st.text_input("Expense Type")
    amt = st.number_input("Amount")

    if st.button("Save Expense"):
        st.session_state.expenses.append({
            "type": exp_type,
            "amount": amt
        })

    st.markdown("### Expense Records")
    st.dataframe(pd.DataFrame(st.session_state.expenses))

# ================= REPORT =================
elif menu == "Reports":

    df = pd.DataFrame({
        "Category":["Collections","Loans","Donations","Expenses"],
        "Amount":[
            sum(x["amount"] for x in st.session_state.collections),
            sum(x["amount"] for x in st.session_state.loans),
            sum(x["amount"] for x in st.session_state.donations),
            sum(x["amount"] for x in st.session_state.expenses)
        ]
    })

    st.bar_chart(df.set_index("Category"))
# ================= USERS =================
elif menu == "Users":

    st.subheader("👤 User Management")

    if st.session_state.role != "Admin":
        st.warning("Only Admin can access this page")
    else:
        if "users" not in st.session_state:
            st.session_state.users = [
                {"username": "admin", "password": "admin123", "role": "Admin"}
            ]

        st.markdown("### ➕ Add User")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Editor", "Viewer"])

        if st.button("Create User"):
            if username and password:
                st.session_state.users.append({
                    "username": username,
                    "password": password,
                    "role": role
                })
                st.success("User Created ✅")
            else:
                st.error("Fill all fields")

        st.markdown("### 📋 Users List")

        for user in st.session_state.users:
            st.write(f"{user['username']} - {user['role']}")

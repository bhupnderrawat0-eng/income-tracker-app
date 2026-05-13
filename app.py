import streamlit as st
import pandas as pd
import hashlib
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# ================= FIREBASE =================
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva AI", layout="wide")

# ================= DARK CSS =================
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}
.block-container {padding-top:0rem;}

.stApp{
background:linear-gradient(135deg,#0f172a,#020617);
}

h1,h2,h3,label{color:white !important;}

.stTextInput input,.stNumberInput input,.stSelectbox div{
background:#111827 !important;
color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        users = db.collection("users").stream()
        enc = hashlib.sha256(pwd.encode()).hexdigest()

        for u in users:
            data = u.to_dict()
            if data["username"] == user and data["password"] == enc:
                st.session_state.login=True
                st.session_state.user=user
                st.session_state.role=data["role"]
                st.rerun()

        st.error("Invalid login")

    st.stop()

# ================= SIDEBAR =================
menu = st.sidebar.radio("Menu",[
    "Dashboard","Customers","Collections","Loans",
    "Reports","Users"
])

st.sidebar.write(f"👤 {st.session_state.user}")
st.sidebar.write(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.login=False
    st.rerun()

# ================= MONTH =================
def get_months():
    return [datetime.date(2026,i,1).strftime("%B %Y") for i in range(1,13)]

# ================= DASHBOARD =================
if menu=="Dashboard":

    col = sum([d.to_dict()["amount"] for d in db.collection("collections").stream()])
    loan = sum([d.to_dict()["amount"] for d in db.collection("loans").stream()])
    cust = len(list(db.collection("customers").stream()))

    c1,c2,c3 = st.columns(3)
    c1.metric("Collections",f"₹ {col}")
    c2.metric("Loans",f"₹ {loan}")
    c3.metric("Customers",cust)

# ================= CUSTOMERS =================
elif menu=="Customers":

    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        db.collection("customers").add({
            "name":name,
            "mobile":mobile
        })

    data = [d.to_dict() for d in db.collection("customers").stream()]
    st.dataframe(pd.DataFrame(data))

# ================= COLLECTION =================
elif menu=="Collections":

    customers = [d.to_dict() for d in db.collection("customers").stream()]

    if customers:
        cust = st.selectbox(
            "Customer",
            customers,
            format_func=lambda x:f"{x['name']} ({x['mobile']})"
        )

        month = st.selectbox("Month", get_months())
        amount = st.number_input("Amount", min_value=0.0)
        date = st.date_input("Collection Date")

        if st.button("Save"):
            db.collection("collections").add({
                "name":cust["name"],
                "month":month,
                "amount":amount,
                "date":str(date)
            })

    data = [d.to_dict() for d in db.collection("collections").stream()]
    st.dataframe(pd.DataFrame(data))

# ================= LOANS =================
elif menu=="Loans":

    customers = [d.to_dict() for d in db.collection("customers").stream()]

    if customers:
        cust = st.selectbox(
            "Customer",
            customers,
            format_func=lambda x:f"{x['name']} ({x['mobile']})"
        )

        amount = st.number_input("Loan Amount", min_value=0.0)
        date = st.date_input("Loan Start Date")

        if st.button("Save Loan"):
            db.collection("loans").add({
                "name":cust["name"],
                "amount":amount,
                "date":str(date)
            })

    data = [d.to_dict() for d in db.collection("loans").stream()]
    st.dataframe(pd.DataFrame(data))

# ================= REPORT =================
elif menu=="Reports":

    col = sum([d.to_dict()["amount"] for d in db.collection("collections").stream()])
    loan = sum([d.to_dict()["amount"] for d in db.collection("loans").stream()])

    df = pd.DataFrame({
        "Type":["Collections","Loans"],
        "Amount":[col,loan]
    })

    st.bar_chart(df.set_index("Type"))

# ================= USERS =================
elif menu=="Users":

    if st.session_state.role!="Admin":
        st.warning("Admin only")
    else:

        user = st.text_input("Username")
        pwd = st.text_input("Password")
        role = st.selectbox("Role",["Admin","Editor","Viewer"])

        if st.button("Add User"):
            enc = hashlib.sha256(pwd.encode()).hexdigest()
            db.collection("users").add({
                "username":user,
                "password":enc,
                "role":role
            })

        data = [d.to_dict() for d in db.collection("users").stream()]
        st.dataframe(pd.DataFrame(data))

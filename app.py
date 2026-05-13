import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime

# ================= CONFIG =================
st.set_page_config(page_title="AI Smart Finance", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}
#MainMenu {visibility:hidden;}

.block-container{
    padding-top:0.5rem !important;
    margin-top:-20px !important;
}

.stApp{
    background:linear-gradient(135deg,#0f172a,#020617);
}

h1,h2,h3,h4,label{color:white !important;}

.stButton>button{
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:10px;
}

.stTextInput input,.stNumberInput input{
    background:#111827 !important;
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= DB =================
conn = sqlite3.connect("smart.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS loans(name TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL)")
conn.commit()

# ================= DEFAULT ADMIN =================
admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
if c.execute("SELECT * FROM users WHERE username='admin'").fetchone() is None:
    c.execute("INSERT INTO users VALUES(?,?,?)",("admin",admin_pass,"Admin"))
    conn.commit()

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        enc = hashlib.sha256(pwd.encode()).hexdigest()
        res = c.execute("SELECT * FROM users WHERE username=? AND password=?", (user,enc)).fetchone()

        if res:
            st.session_state.login = True
            st.session_state.user = user
            st.session_state.role = res[2]
            st.rerun()
        else:
            st.error("Wrong login")

    st.stop()

# ================= SIDEBAR =================
st.sidebar.title("🚀 Bal Yuva AI")

menu = st.sidebar.radio("Menu",[
    "Dashboard","Customers","Collections","Loans",
    "Donations","Expenses","Reports","Users","AI Insights"
])

st.sidebar.write(f"👤 {st.session_state.user}")
st.sidebar.write(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()

# ================= MONTH =================
def get_months():
    return [datetime.date(2026,i,1).strftime("%B %Y") for i in range(1,13)]

# ================= DASHBOARD =================
if menu == "Dashboard":

    col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
    cust = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Collections",f"₹ {col}")
    c2.metric("Donations",f"₹ {don}")
    c3.metric("Expenses",f"₹ {exp}")
    c4.metric("Customers",cust)

    st.metric("Balance",f"₹ {col+don-exp}")

# ================= CUSTOMERS =================
elif menu == "Customers":

    name = st.text_input("Name")
    mobile = st.text_input("Mobile")
    date = st.date_input("Start Date")

    if st.button("Add"):
        c.execute("INSERT INTO customers VALUES(?,?,?)",(name,mobile,str(date)))
        conn.commit()

    df = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df)

# ================= COLLECTION =================
elif menu == "Collections":

    dfc = pd.read_sql("SELECT * FROM customers", conn)

    if dfc.empty:
        st.warning("Add customers first")
    else:
        cust = st.selectbox("Customer", dfc.to_dict("records"),
                            format_func=lambda x:f"{x['name']} ({x['mobile']})")

        month = st.selectbox("Month", get_months())
        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            c.execute("INSERT INTO collections VALUES(?,?,?)",(cust["name"],month,amt))
            conn.commit()

    df = pd.read_sql("SELECT * FROM collections", conn)
    st.dataframe(df)

# ================= LOANS =================
elif menu == "Loans":

    name = st.text_input("Name")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Add"):
        c.execute("INSERT INTO loans VALUES(?,?)",(name,amt))
        conn.commit()

    df = pd.read_sql("SELECT * FROM loans", conn)
    st.dataframe(df)

# ================= DONATION =================
elif menu == "Donations":

    name = st.text_input("Donor")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        c.execute("INSERT INTO donations VALUES(?,?)",(name,amt))
        conn.commit()

    df = pd.read_sql("SELECT * FROM donations", conn)
    st.dataframe(df)

# ================= EXPENSE =================
elif menu == "Expenses":

    typ = st.text_input("Type")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Save"):
        c.execute("INSERT INTO expenses VALUES(?,?)",(typ,amt))
        conn.commit()

    df = pd.read_sql("SELECT * FROM expenses", conn)
    st.dataframe(df)

# ================= USERS =================
elif menu == "Users":

    if st.session_state.role != "Admin":
        st.warning("Admin only")
    else:
        user = st.text_input("Username")
        pwd = st.text_input("Password")
        role = st.selectbox("Role",["Admin","Editor","Viewer"])

        if st.button("Add User"):
            enc = hashlib.sha256(pwd.encode()).hexdigest()
            c.execute("INSERT INTO users VALUES(?,?,?)",(user,enc,role))
            conn.commit()

        df = pd.read_sql("SELECT username,role FROM users", conn)
        st.dataframe(df)

# ================= REPORT =================
elif menu == "Reports":

    data = pd.DataFrame({
        "Type":["Collections","Donations","Expenses"],
        "Amount":[
            c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0,
            c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
        ]
    })

    st.bar_chart(data.set_index("Type"))

# ================= AI =================
elif menu == "AI Insights":

    col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    st.title("🤖 AI Smart Insights")

    if col == 0:
        st.warning("No data yet")
    else:
        if exp > col:
            st.error("⚠️ Expenses are higher than collections")
        elif col > exp:
            st.success("✅ Good financial health")

        st.write(f"💡 Savings Potential: ₹ {col - exp}")

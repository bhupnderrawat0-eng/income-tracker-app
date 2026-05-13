import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva Smart Finance", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}

.stApp{
background:linear-gradient(135deg,#0f172a,#020617);
font-family: 'Segoe UI', sans-serif;
}

.block-container{
padding-top:1rem;
}

h1,h2,h3{
color:white !important;
font-weight:700;
}

/* Sidebar */
section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#111827,#020617);
}

/* Inputs */
.stTextInput input,.stNumberInput input,.stSelectbox div{
background:#111827 !important;
color:white !important;
border-radius:10px;
}

/* Card */
.card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:20px;
margin-bottom:15px;
border:1px solid rgba(255,255,255,0.08);
box-shadow:0 8px 25px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ================= DB =================
conn = sqlite3.connect("automation.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, amount REAL, date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS loans(name TEXT, amount REAL, date TEXT)")
conn.commit()

# ================= ADMIN =================
admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
if not c.execute("SELECT * FROM users WHERE username='admin'").fetchone():
    c.execute("INSERT INTO users VALUES(?,?,?)",("admin",admin_pass,"Admin"))
    conn.commit()

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<h1 style='text-align:center;'>🔐 Smart Login</h1>", unsafe_allow_html=True)

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        enc = hashlib.sha256(p.encode()).hexdigest()
        res = c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,enc)).fetchone()

        if res:
            st.session_state.login=True
            st.session_state.user=u
            st.session_state.role=res[2]
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# ================= SIDEBAR =================
st.sidebar.markdown("## 🚀 Bal Yuva AI")
menu = st.sidebar.radio("",[
    "Dashboard","Customers","Collections","Loans","Reports","Users","AI Insights"
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

    col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0
    cust = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

    st.markdown("""
    <div class="card">
    <h2>🚀 Bal Yuva Mangal Dal</h2>
    <p>Smart Automated Finance Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    c1.metric("Collections",f"₹ {col}")
    c2.metric("Loans",f"₹ {loan}")
    c3.metric("Customers",cust)

# ================= CUSTOMERS =================
elif menu=="Customers":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile")

    if st.button("Add Customer"):
        c.execute("INSERT INTO customers VALUES(?,?)",(name,mobile))
        conn.commit()

    st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df)

# ================= COLLECTION =================
elif menu=="Collections":

    dfc = pd.read_sql("SELECT * FROM customers", conn)

    if not dfc.empty:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        cust = st.selectbox("Customer", dfc.to_dict("records"),
                            format_func=lambda x:f"{x['name']} ({x['mobile']})")

        month = st.selectbox("Month", get_months())
        amt = st.number_input("Amount", min_value=0.0)
        date = st.date_input("Collection Date")

        if st.button("Save Collection"):
            c.execute("INSERT INTO collections VALUES(?,?,?,?)",
                      (cust["name"],month,amt,str(date)))
            conn.commit()

        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql("SELECT * FROM collections", conn)
    st.dataframe(df)

# ================= LOANS =================
elif menu=="Loans":

    dfc = pd.read_sql("SELECT * FROM customers", conn)

    if not dfc.empty:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        cust = st.selectbox("Customer", dfc.to_dict("records"),
                            format_func=lambda x:f"{x['name']} ({x['mobile']})")

        amt = st.number_input("Loan Amount", min_value=0.0)
        date = st.date_input("Loan Start Date")

        if st.button("Save Loan"):
            c.execute("INSERT INTO loans VALUES(?,?,?)",
                      (cust["name"],amt,str(date)))
            conn.commit()

        st.markdown('</div>', unsafe_allow_html=True)

    df = pd.read_sql("SELECT * FROM loans", conn)
    st.dataframe(df)

# ================= REPORT =================
elif menu=="Reports":

    col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0

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
            c.execute("INSERT INTO users VALUES(?,?,?)",(user,enc,role))
            conn.commit()

        df = pd.read_sql("SELECT username,role FROM users", conn)
        st.dataframe(df)

# ================= AI INSIGHTS =================
elif menu=="AI Insights":

    col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.title("🤖 Smart Insights")

    if col == 0:
        st.warning("No data yet")

    else:
        if loan > col:
            st.error("⚠️ Loan amount is higher than collection")
        else:
            st.success("✅ Financial condition is stable")

        st.write(f"💡 Net Strength: ₹ {col - loan}")

    st.markdown('</div>', unsafe_allow_html=True)

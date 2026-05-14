import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS collections(name TEXT, month TEXT, start_date TEXT, date TEXT, amount REAL)")
    c.execute("""
CREATE TABLE IF NOT EXISTS loans (
    name TEXT,
    amount REAL,
    interest_rate REAL,
    start_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS loan_payments (
    name TEXT,
    date TEXT,
    amount REAL
)
""")

    # UPDATED
    c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL, date TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
    conn.commit()

create_tables()

# SAFE column add
def safe_add_column(table, column):
    try:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")
    except:
        pass

safe_add_column("donations", "date")
safe_add_column("expenses", "date")

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# default admin
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users VALUES (?,?,?)", ("admin", hash_pass("admin123"), "Admin"))
    conn.commit()

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

/* MOBILE FIX */
html, body, .stApp {
    overflow-y:auto !important;
    overflow-x:hidden !important;
    height:auto !important;
}

/* mobile scroll menu */
.stRadio > div {
    flex-direction: row;
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, hash_pass(p))
        ).fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user[0]
            st.session_state.role = user[2]
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ================= DEVICE DETECTION (FINAL FIX) =================
user_agent = st.context.headers.get("user-agent", "").lower()

if "android" in user_agent or "iphone" in user_agent:
    is_mobile = True
else:
    is_mobile = False

# ================= MENU =================
if not is_mobile:
    with st.sidebar:
        st.markdown("## 🚀 Bal Yuva SaaS")

        menu = option_menu(
            None,
            ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"],
            icons=["house","people","cash","bank","gift","credit-card","bar-chart","person","robot"],
            default_index=0,
        )
else:
    st.markdown("### 🚀 Bal Yuva SaaS")

    menu = st.radio(
        "Navigation",
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users","AI"],
        horizontal=True
    )

# ================= USER BAR =================
col_user, col_logout = st.columns([3,1])

with col_user:
    st.write(f"👤 {st.session_state.current_user}")

with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("---")

# ================= HEADER =================
st.markdown("""
<div style="background:rgba(0,0,0,0.4);padding:15px;border-radius:12px;margin-bottom:20px;">
<h2 style='color:white;'>🚀 Bal Yuva Mangal Dal</h2>
<p style='color:lightgray;'>Smart Finance SaaS System</p>
</div>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================
if menu == "Dashboard":

    total_col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    total_loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0
    total_don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    total_exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("Loans", f"₹ {total_loan}")
    c3.metric("Donations", f"₹ {total_don}")
    c4.metric("Expenses", f"₹ {total_exp}")

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")
# ========================= CUSTOMERS =========================
elif menu == "Customers":

    st.subheader("👤 Customer Management")

    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile")
    start_date = st.date_input("Start Date")

    if st.button("Add Customer"):
        c.execute(
            "INSERT INTO customers (name, mobile, start_date) VALUES (?,?,?)",
            (name, mobile, start_date.strftime("%Y-%m-%d"))
        )
        conn.commit()
        st.success("Customer Added ✅")
        st.rerun()

    df = pd.read_sql("SELECT rowid as id, * FROM customers", conn)
    st.dataframe(df)

    if not df.empty:
        selected_id = st.selectbox("Select Customer", df["id"])
        row = df[df["id"] == selected_id].iloc[0]

        new_name = st.text_input("Edit Name", value=row["name"])
        new_mobile = st.text_input("Edit Mobile", value=row["mobile"])
        new_start = st.date_input(
            "Edit Start Date",
            value=pd.to_datetime(row["start_date"])
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Customer"):
                c.execute(
                    "UPDATE customers SET name=?, mobile=?, start_date=? WHERE rowid=?",
                    (
                        new_name,
                        new_mobile,
                        new_start.strftime("%Y-%m-%d"),
                        selected_id
                    )
                )
                conn.commit()
                st.success("Updated ✅")
                st.rerun()

        with col2:
            if st.button("Delete Customer"):
                c.execute("DELETE FROM customers WHERE rowid=?", (selected_id,))
                conn.commit()
                st.warning("Deleted ⚠️")
                st.rerun()

# ========================= COLLECTION =========================
elif menu == "Collections":

    st.subheader("🔥 Collection Management")

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if customers.empty:
        st.warning("No customers available")
    else:
        cust = st.selectbox("Customer", customers["name"])

        month = st.selectbox(
            "Month",
            [datetime.date(2026, m, 1).strftime("%B %Y") for m in range(1, 13)]
        )

        payment_date = st.date_input("Payment Date")
        amt = st.number_input("Amount")

        if st.button("Save Collection"):

            start_date = customers[customers["name"] == cust]["start_date"].values[0]

            c.execute(
                "INSERT INTO collections (name, month, start_date, date, amount) VALUES (?,?,?,?,?)",
                (
                    cust,
                    month,
                    start_date,
                    payment_date.strftime("%Y-%m-%d"),
                    amt
                )
            )
            conn.commit()
            st.success("Collection Saved ✅")
            st.rerun()

        # SHOW DATA
        df = pd.read_sql("SELECT rowid as id, * FROM collections", conn)
        st.dataframe(df)

        # MANAGE
        if not df.empty:
            df["label"] = df["name"] + " | " + df["month"] + " | ₹" + df["amount"].astype(str)

            selected = st.selectbox("Select Entry", df["label"])
            row = df[df["label"] == selected].iloc[0]

            new_amt = st.number_input("Edit Amount", value=float(row["amount"]))

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Update Collection"):
                    c.execute(
                        "UPDATE collections SET amount=? WHERE rowid=?",
                        (new_amt, row["id"])
                    )
                    conn.commit()
                    st.success("Updated ✅")
                    st.rerun()

            with col2:
                if st.button("Delete Collection"):
                    c.execute("DELETE FROM collections WHERE rowid=?", (row["id"],))
                    conn.commit()
                    st.warning("Deleted ⚠️")
                    st.rerun()

            # DELETE ALL
            if st.button("Delete All Collections of This Customer"):
                c.execute("DELETE FROM collections WHERE name=?", (row["name"],))
                conn.commit()
                st.error("All Deleted ❌")
                st.rerun()

# ========================= LOANS =========================
elif menu == "Loans":

    st.subheader("💰 Loan Management")

    # ================= LOAD CUSTOMERS =================
    customers = pd.read_sql("SELECT * FROM customers", conn)

    if customers.empty:
        st.warning("No customers available. Add customers first.")
    else:
        cust = st.selectbox("Customer", customers["name"])

        loan_amt = st.number_input("Loan Amount", min_value=0.0)
        interest_rate = st.number_input("Interest % per month", min_value=0.0, value=1.0)
        loan_date = st.date_input("Loan Start Date")

        # ================= ADD LOAN =================
        if st.button("Add Loan"):
            c.execute(
                "INSERT INTO loans (name, amount, interest_rate, start_date) VALUES (?,?,?,?)",
                (
                    cust,
                    loan_amt,
                    interest_rate,
                    loan_date.strftime("%Y-%m-%d")
                )
            )
            conn.commit()
            st.success("Loan Added ✅")
            st.rerun()

    # ================= LOAD LOANS =================
    loans_df = pd.read_sql("SELECT rowid as id, * FROM loans", conn)

    if not loans_df.empty:

        # 🔥 FIX: dynamic column detect
        amount_col = "amount" if "amount" in loans_df.columns else "total_amount"

        loans_df["display"] = loans_df["name"] + " | ₹" + loans_df[amount_col].astype(str)

        # ================= PAYMENT =================
        st.markdown("---")
        st.subheader("💸 Loan Payment")

        selected = st.selectbox("Select Loan", loans_df["display"])
        selected_row = loans_df[loans_df["display"] == selected].iloc[0]

        pay_amt = st.number_input("Payment Amount", min_value=0.0)
        pay_date = st.date_input("Payment Date")

        if st.button("Add Payment"):
            c.execute(
                "INSERT INTO loan_payments (name, date, amount) VALUES (?,?,?)",
                (
                    selected_row["name"],
                    pay_date.strftime("%Y-%m-%d"),
                    pay_amt
                )
            )
            conn.commit()
            st.success("Payment Added ✅")
            st.rerun()

        # ================= DELETE LOAN =================
        if st.button("Delete Loan"):
            c.execute("DELETE FROM loans WHERE rowid=?", (selected_row["id"],))
            conn.commit()
            st.warning("Loan Deleted ❌")
            st.rerun()

    # ================= SUMMARY =================
    st.markdown("---")
    st.subheader("📊 Loan Summary (Simple Interest)")

    loans_df = pd.read_sql("SELECT * FROM loans", conn)
    payments_df = pd.read_sql("SELECT * FROM loan_payments", conn)

    result = []

    for _, loan in loans_df.iterrows():

        name = loan["name"]
        amount_col = "amount" if "amount" in loan else "total_amount"

        principal = loan[amount_col]
        rate = loan["interest_rate"]
        start_date = pd.to_datetime(loan["start_date"])
        today = pd.to_datetime(datetime.date.today())

        months = (today.year - start_date.year) * 12 + (today.month - start_date.month)

        cust_payments = payments_df[payments_df["name"] == name]

        balance = principal
        total_paid = cust_payments["amount"].sum()

        total_interest = 0

        for m in range(months):
            interest = balance * (rate / 100)
            total_interest += interest

            if m < len(cust_payments):
                balance -= cust_payments.iloc[m]["amount"]

        balance = principal - total_paid

        result.append({
            "Name": name,
            "Principal": principal,
            "Interest %": rate,
            "Total Paid": total_paid,
            "Total Interest": round(total_interest, 2),
            "Remaining Balance": round(balance, 2)
        })

    if result:
        st.dataframe(pd.DataFrame(result))
    else:
        st.info("No loan data available")
# ================= DONATIONS =================
elif menu == "Donations":

    donor = st.text_input("Donor Name")
    date = st.date_input("Date")
    amt = st.number_input("Amount")

    if st.button("Save Donation"):
        c.execute("INSERT INTO donations VALUES (?,?,?)",
                  (donor, amt, date.strftime("%Y-%m-%d")))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM donations", conn))

# ================= EXPENSES =================
elif menu == "Expenses":

    exp = st.text_input("Expense Type")
    date = st.date_input("Date")
    amt = st.number_input("Amount")

    if st.button("Save Expense"):
        c.execute("INSERT INTO expenses VALUES (?,?,?)",
                  (exp, amt, date.strftime("%Y-%m-%d")))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM expenses", conn))
# ================= REPORT =================
elif menu == "Reports":

    st.subheader("📊 Advanced Reports")

    df = pd.read_sql("SELECT * FROM collections", conn)

    if not df.empty:

        # ================= MONTH FILTER =================
        month_list = sorted(df["month"].unique())
        selected_month = st.selectbox("Select Month", month_list)

        df_month = df[df["month"] == selected_month]

        # ================= SUMMARY =================
        st.markdown("### 📅 Monthly Summary")

        total_collection = df_month["amount"].sum()

        expense_df = pd.read_sql("SELECT * FROM expenses", conn)
        total_expense = expense_df["amount"].sum() if not expense_df.empty else 0

        donation_df = pd.read_sql("SELECT * FROM donations", conn)
        total_donation = donation_df["amount"].sum() if not donation_df.empty else 0

        balance = total_collection + total_donation - total_expense

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Collection", f"₹ {total_collection}")
        c2.metric("Donations", f"₹ {total_donation}")
        c3.metric("Expenses", f"₹ {total_expense}")
        c4.metric("Balance", f"₹ {balance}")

        # ================= CHART =================
        st.markdown("### 📊 Collection Chart")

        chart_df = df_month.copy()
        chart_df["date"] = pd.to_datetime(chart_df["date"])

        st.bar_chart(chart_df.set_index("date")["amount"])

        # ================= CUSTOMER REPORT =================
        st.markdown("### 👤 Customer-wise Report")

        customer_summary = df_month.groupby("name")["amount"].sum().reset_index()
        st.dataframe(customer_summary)

        # ================= TOP CONTRIBUTORS =================
        st.markdown("### 🏆 Top Contributors")

        top_users = customer_summary.sort_values(by="amount", ascending=False).head(5)
        st.dataframe(top_users)

        # ================= 🔔 SMART REMINDER SYSTEM =================
        st.markdown("### 🔔 Smart Reminder System")

        all_customers = pd.read_sql("SELECT * FROM customers", conn)

        paid_customers = df_month["name"].unique()

        pending_list = all_customers[
            ~all_customers["name"].isin(paid_customers)
        ]

        if not pending_list.empty:

            total_pending = len(pending_list)

            if total_pending >= 5:
                st.error(f"🚨 High Pending: {total_pending} customers")
            elif total_pending >= 2:
                st.warning(f"⚠️ Medium Pending: {total_pending} customers")
            else:
                st.info(f"ℹ️ Low Pending: {total_pending} customers")

            st.dataframe(pending_list)

            # ================= WHATSAPP REMINDER =================
            st.markdown("### 📱 Send Reminder")

            selected_customer = st.selectbox(
                "Select Customer",
                pending_list["name"]
            )

            mobile = pending_list[
                pending_list["name"] == selected_customer
            ]["mobile"].values[0]

            message = f"Hello {selected_customer}, aapka payment pending hai. Kripya jaldi jama karein."

            whatsapp_url = f"https://wa.me/{mobile}?text={message}"

            st.markdown(
                f"[👉 Send WhatsApp Reminder]({whatsapp_url})",
                unsafe_allow_html=True
            )

        else:
            st.success("✅ All customers have paid for this month")

        # ================= 📥 EXPORT TO EXCEL =================
        st.markdown("### 📥 Download Report")

        import io

        report_df = df_month.copy()   # ✅ FIXED

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            report_df.to_excel(writer, index=False, sheet_name='Report')

        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name="monthly_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("No collection data available yet")
# ================= USERS =================
if menu == "Users":

    if st.session_state.role != "Admin":
        st.warning("Only Admin Access")
    else:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        r = st.selectbox("Role", ["Admin","Editor","Viewer"])

        if st.button("Create User"):
            c.execute("INSERT INTO users VALUES (?,?,?)",(u,hash_pass(p),r))
            conn.commit()
            st.success("User Created")

        st.dataframe(pd.read_sql("SELECT username, role FROM users", conn))

# ================= AI =================
elif menu == "AI":
    st.subheader("🤖 AI Insights (Coming Soon)")
    st.info("Future AI features yaha add honge")

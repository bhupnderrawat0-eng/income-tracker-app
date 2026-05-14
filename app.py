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
    c.execute("CREATE TABLE IF NOT EXISTS customers(name TEXT, mobile TEXT, start_date TEXT)")
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

    c.execute("CREATE TABLE IF NOT EXISTS donations(name TEXT, amount REAL, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS expenses(type TEXT, amount REAL, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")

    conn.commit()

create_tables()

# ================= CONFIG =================
st.set_page_config(page_title="Bal Yuva SaaS", layout="wide")

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
            (u, hashlib.sha256(p.encode()).hexdigest())
        ).fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user[0]
            st.session_state.role = user[2]
            st.rerun()
        else:
            st.error("Invalid Login")
    st.stop()

# ================= MENU =================
with st.sidebar:
    menu = option_menu(
        "Menu",
        ["Dashboard","Customers","Collections","Loans","Donations","Expenses","Reports","Users"],
        icons=["house","people","cash","bank","gift","credit-card","bar-chart","person"],
        default_index=0,
    )

# ================= DASHBOARD =================
if menu == "Dashboard":
    total_col = c.execute("SELECT SUM(amount) FROM collections").fetchone()[0] or 0
    total_loan = c.execute("SELECT SUM(amount) FROM loans").fetchone()[0] or 0
    total_don = c.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    total_exp = c.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

# ================= CUSTOMERS =================
elif menu == "Customers":
    name = st.text_input("Name")
    mobile = st.text_input("Mobile")
    start_date = st.date_input("Start Date")

    if st.button("Add Customer"):
        c.execute("INSERT INTO customers VALUES (?,?,?)",
                  (name, mobile, start_date.strftime("%Y-%m-%d")))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM customers", conn))

# ================= COLLECTIONS =================
elif menu == "Collections":
    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:
        cust = st.selectbox("Customer", customers["name"])
        month = st.selectbox("Month", [datetime.date(2026,m,1).strftime("%B %Y") for m in range(1,13)])
        date = st.date_input("Payment Date")
        amt = st.number_input("Amount")

        if st.button("Save Collection"):
            start = customers[customers["name"] == cust]["start_date"].values[0]

            c.execute("INSERT INTO collections VALUES (?,?,?,?,?)",
                      (cust, month, start, date.strftime("%Y-%m-%d"), amt))
            conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM collections", conn))

# ================= LOANS =================
elif menu == "Loans":

    st.subheader("💰 Loan Management")

    customers = pd.read_sql("SELECT * FROM customers", conn)

    if not customers.empty:
        cust = st.selectbox("Customer", customers["name"])
        amt = st.number_input("Loan Amount")
        rate = st.number_input("Interest % per month", value=1.0)
        date = st.date_input("Start Date")

        if st.button("Add Loan"):
            c.execute(
                "INSERT INTO loans (name, amount, interest_rate, start_date) VALUES (?,?,?,?)",
                (cust, amt, rate, date.strftime("%Y-%m-%d"))
            )
            conn.commit()
            st.success("Loan Added")

    st.markdown("---")

    loans_df = pd.read_sql("SELECT * FROM loans", conn)
    payments_df = pd.read_sql("SELECT * FROM loan_payments", conn)

    if not loans_df.empty:

        st.subheader("💸 Loan Payment")

        loans_df["label"] = loans_df["name"] + " | ₹" + loans_df["amount"].astype(str)
        selected = st.selectbox("Select Loan", loans_df["label"])

        pay_amt = st.number_input("Payment Amount")
        pay_date = st.date_input("Payment Date")

        if st.button("Add Payment"):
            name = selected.split(" | ")[0]

            c.execute("INSERT INTO loan_payments VALUES (?,?,?)",
                      (name, pay_date.strftime("%Y-%m-%d"), pay_amt))
            conn.commit()
            st.success("Payment Added")

    st.markdown("---")

    st.subheader("📊 Loan Summary")

    result = []

    for _, loan in loans_df.iterrows():
        name = loan["name"]
        principal = loan["amount"]
        rate = loan["interest_rate"]

        start = pd.to_datetime(loan["start_date"])
        today = pd.to_datetime(datetime.date.today())

        months = max(1, (today.year - start.year)*12 + (today.month - start.month))

        paid = payments_df[payments_df["name"] == name]["amount"].sum()

        interest = principal * (rate/100) * months
        total = principal + interest
        balance = total - paid

        result.append({
            "Name": name,
            "Loan": principal,
            "Interest %": rate,
            "Months": months,
            "Interest": round(interest,2),
            "Paid": paid,
            "Balance": round(balance,2)
        })

    st.dataframe(pd.DataFrame(result))

# ================= DONATIONS =================
elif menu == "Donations":
    name = st.text_input("Donor")
    date = st.date_input("Date")
    amt = st.number_input("Amount")

    if st.button("Save"):
        c.execute("INSERT INTO donations VALUES (?,?,?)",
                  (name, amt, date.strftime("%Y-%m-%d")))
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM donations", conn))

# ================= EXPENSES =================
elif menu == "Expenses":
    typ = st.text_input("Type")
    date = st.date_input("Date")
    amt = st.number_input("Amount")

    if st.button("Save"):
        c.execute("INSERT INTO expenses VALUES (?,?,?)",
                  (typ, amt, date.strftime("%Y-%m-%d")))
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

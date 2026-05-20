import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# ================= SUPABASE =================
from supabase import create_client, Client

SUPABASE_URL = "https://eflpyuvwtofgnjcrsgoz.supabase.co"
SUPABASE_KEY = "sb_publishable_FwNyrhViDcmux8hRRidMmA_Ta4EGAyf"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= SAFE LOAD =================
try:
    loans_data = supabase.table("loans").select("*").execute()
    loans_df = pd.DataFrame(loans_data.data)
except:
    loans_df = pd.DataFrame()

# ================= PASSWORD =================
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()


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

    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if u == "" or p == "":
                st.warning("Enter Username & Password")
            else:
                try:
                    user_data = supabase.table("users") \
                        .select("*") \
                        .eq("username", u) \
                        .execute()

                    if user_data.data:
                        user = user_data.data[0]

                        if user["password"] == hash_pass(p):

                            st.session_state.logged_in = True
                            st.session_state.current_user = user["username"]
                            st.session_state.role = user["role"]

                            st.rerun()
                        else:
                            st.error("Wrong Password")
                    else:
                        st.error("User not found")

                except Exception as e:
                    st.error(f"Login Error: {e}")

    st.stop()

# ================= ROLE SETUP =================
role = st.session_state.get("role", None)

is_admin = role == "Admin"
is_editor = role == "Editor"
is_viewer = role == "Viewer"
# ================= DEVICE DETECTION (FINAL FIX) =================
user_agent = st.context.headers.get("user-agent", "").lower()

if "android" in user_agent or "iphone" in user_agent:
    is_mobile = True
else:
    is_mobile = False

# ================= ROLE BASED MENU =================
if is_admin:
    menu_list = ["Dashboard","Customers","Collections","loans","Donations","Expenses","Reports","Users","AI"]
elif is_editor:
    menu_list = ["Dashboard","Customers","Collections","loans","Donations","Expenses","Reports"]
else:
    menu_list = ["Dashboard","Reports"]


# ================= MENU =================
if not is_mobile:
    with st.sidebar:
        st.markdown("## 🚀 Bal Yuva SaaS")

        menu = option_menu(
            None,
            menu_list,
            icons=["house","people","cash","bank","gift","credit-card","bar-chart","person","robot"][:len(menu_list)],
            default_index=0,
        )
else:
    st.markdown("### 🚀 Bal Yuva SaaS")

    menu = st.radio(
        "Navigation",
        menu_list,
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

    def get_sum(table_name):
        try:
            data = supabase.table(table_name).select("amount").execute()
            df = pd.DataFrame(data.data)
            return df["amount"].sum() if not df.empty else 0
        except:
            return 0

    total_col = get_sum("collections")
    total_loan = get_sum("loans")
    total_don = get_sum("donations")
    total_exp = get_sum("expenses")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("loans", f"₹ {total_loan}")
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
        try:
            supabase.table("customers").insert({
                "name": name,
                "mobile": mobile,
                "start_date": start_date.strftime("%Y-%m-%d")
            }).execute()

            st.success("Customer Added ✅")
            st.rerun()
        except:
            st.error("Error adding customer")

    # LOAD DATA
    try:
        data = supabase.table("customers").select("*").execute()
        df = pd.DataFrame(data.data)
    except:
        df = pd.DataFrame()

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
                try:
                    supabase.table("customers").update({
                        "name": new_name,
                        "mobile": new_mobile,
                        "start_date": new_start.strftime("%Y-%m-%d")
                    }).eq("id", selected_id).execute()

                    st.success("Updated ✅")
                    st.rerun()
                except:
                    st.error("Update failed")

        with col2:
            if st.button("Delete Customer"):
                try:
                    supabase.table("customers").delete().eq("id", selected_id).execute()

                    st.warning("Deleted ⚠️")
                    st.rerun()
                except:
                    st.error("Delete failed")
# ========================= COLLECTION =========================
elif menu == "Collections":

    st.subheader("🔥 Collection Management")

    # LOAD CUSTOMERS
    try:
        cust_data = supabase.table("customers").select("*").execute()
        customers = pd.DataFrame(cust_data.data)
    except:
        customers = pd.DataFrame()

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

        if not is_viewer:
            if st.button("Save Collection"):

                start_date = customers[customers["name"] == cust]["start_date"].values[0]

                try:
                    supabase.table("collections").insert({
                        "name": cust,
                        "month": month,
                        "start_date": start_date,
                        "date": payment_date.strftime("%Y-%m-%d"),
                        "amount": amt
                    }).execute()

                    st.success("Collection Saved ✅")
                    st.rerun()
                except:
                    st.error("Error saving collection")

    # LOAD COLLECTION DATA
    try:
        data = supabase.table("collections").select("*").execute()
        df = pd.DataFrame(data.data)
    except:
        df = pd.DataFrame()

    st.dataframe(df)

    if not df.empty:

        df["label"] = df["name"] + " | " + df["month"] + " | ₹" + df["amount"].astype(str)

        selected = st.selectbox("Select Entry", df["label"])
        row = df[df["label"] == selected].iloc[0]

        new_amt = st.number_input("Edit Amount", value=float(row["amount"]))

        col1, col2 = st.columns(2)

        with col1:
            if not is_viewer:
                if st.button("Update Collection"):
                    try:
                        supabase.table("collections").update({
                            "amount": new_amt
                        }).eq("id", row["id"]).execute()

                        st.success("Updated ✅")
                        st.rerun()
                    except:
                        st.error("Update failed")

        with col2:
            if is_admin:
                if st.button("Delete Collection"):
                    try:
                        supabase.table("collections").delete().eq("id", row["id"]).execute()

                        st.warning("Deleted ⚠️")
                        st.rerun()
                    except:
                        st.error("Delete failed")
# ========================= LOANS =========================
elif menu == "loans":

    st.subheader("💰 Loan Management")

    # LOAD DATA
    try:
        customers = pd.DataFrame(supabase.table("customers").select("*").execute().data)
    except:
        customers = pd.DataFrame()

    try:
        loans_df = pd.DataFrame(supabase.table("loans").select("*").execute().data)
    except:
        loans_df = pd.DataFrame()

    try:
        payments_df = pd.DataFrame(supabase.table("loan_payments").select("*").execute().data)
    except:
        payments_df = pd.DataFrame()

    # ===== ADD LOAN =====
    st.markdown("### ➕ Add Loan")

    if customers.empty:
        st.warning("No customers found")
    else:
        cust = st.selectbox("Customer", customers["name"])
        loan_amt = st.number_input("Loan Amount", min_value=0.0)
        interest_rate = st.number_input("Interest % per month", value=1.0)
        loan_date = st.date_input("Loan Start Date")

        if not is_viewer:
            if st.button("Add Loan", key="add_loan_btn"):
                try:
                    supabase.table("loans").insert({
                        "customer_name": cust,
                        "amount": loan_amt,
                        "interest_rate": interest_rate,
                        "start_date": loan_date.strftime("%Y-%m-%d")
                    }).execute()

                    st.success("Loan Added ✅")
                    st.rerun()
                except:
                    st.error("Error adding loan")

    st.markdown("---")

    # ===== SHOW EXISTING LOANS =====
    if not loans_df.empty:
        st.markdown("📌 Existing loans:")
        for _, row in loans_df.iterrows():
            st.write(f"Loan ID: {row['id']} | {row['customer_name']} | ₹{row['amount']}")

    # ===== SELECT LOAN =====
    if loans_df.empty:
        st.info("No loans available")
        st.stop()

    loans_df["label"] = loans_df.apply(
        lambda x: f"{x['customer_name']} | Loan #{int(x['id'])} | ₹{x['amount']}",
        axis=1
    )

    selected = st.selectbox("Select Loan", loans_df["label"])
    loan_id = int(selected.split("|")[1].replace("Loan #", "").strip())

    loan_row = loans_df[loans_df["id"].astype(int) == loan_id]

    if loan_row.empty:
        st.error("Loan not found")
        st.stop()

    loan = loan_row.iloc[0]

    # ===== ADD PAYMENT =====
    st.markdown("### ➕ Add Payment")

    if not is_viewer:
        pay_amt = st.number_input("Payment Amount", min_value=0.0)
        pay_date = st.date_input("Payment Date")

        if st.button("Add Payment", key="add_payment_btn"):
            if pay_amt > 0:
                try:
                    supabase.table("loan_payments").insert({
                        "loan_id": loan_id,
                        "amount": pay_amt,
                        "date": pay_date.strftime("%Y-%m-%d")
                    }).execute()

                    st.success("Payment Added ✅")
                    st.rerun()
                except:
                    st.error("Error adding payment")

    # ===== SUMMARY + MONTHLY SYSTEM =====
    from datetime import datetime

    principal = loan["amount"]
    rate = loan["interest_rate"]

    cust_payments = payments_df[payments_df["loan_id"] == loan_id].sort_values("date")
    total_paid = cust_payments["amount"].sum() if not cust_payments.empty else 0

    start_date = loan["start_date"]
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    today = datetime.today()

    # ===== MONTHLY BREAKDOWN =====
    timeline = []
    current_date = start_date
    running_principal = principal

    payment_map = {}
    for _, p in cust_payments.iterrows():
        payment_map.setdefault(p["date"][:7], 0)
        payment_map[p["date"][:7]] += p["amount"]

    while current_date <= today:

        month_str = current_date.strftime("%Y-%m")

        principal_before = running_principal
        interest = (principal_before * rate) / 100
        payment = payment_map.get(month_str, 0)

        balance_after = principal_before + interest - payment
        running_principal = balance_after

        timeline.append({
            "Month": current_date.strftime("%b %Y"),
            "Principal": round(principal_before, 2),
            "Interest": round(interest, 2),
            "Payment": payment,
            "Balance": round(balance_after, 2)
        })

        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year+1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month+1)

    total_interest = sum(x["Interest"] for x in timeline)
    balance = timeline[-1]["Balance"] if timeline else principal

    # ===== DISPLAY =====
    st.markdown("### 📊 Loan Summary")
    st.write(f"Principal: ₹{principal}")
    st.write(f"Total Paid: ₹{total_paid}")
    st.write(f"Total Interest: ₹{round(total_interest, 2)}")
    st.write(f"Balance: ₹{round(balance, 2)}")

    st.markdown("### 📅 Monthly Breakdown")
    timeline_df = pd.DataFrame(timeline)
    st.dataframe(timeline_df)

    # ===== DELETE =====
    st.markdown("---")

    if is_admin:
        if st.button("Delete Loan", key="delete_loan_btn"):
            try:
                supabase.table("loans").delete().eq("id", loan_id).execute()
                supabase.table("loan_payments").delete().eq("loan_id", loan_id).execute()

                st.success("Loan Deleted 🗑️")
                st.rerun()
            except:
                st.error("Delete failed")
# ================= DONATIONS =================
elif menu == "Donations":

    st.subheader("🎁 Donations Management")

    # ===== ADD DONATION =====
    if not is_viewer:
        donor = st.text_input("Donor Name")
        date = st.date_input("Date")
        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save Donation", key="save_donation"):
            if donor and amt > 0:
                try:
                    supabase.table("donations").insert({
                        "name": donor,
                        "amount": amt,
                        "date": date.strftime("%Y-%m-%d")
                    }).execute()

                    st.success("Donation Saved ✅")
                    st.rerun()
                except:
                    st.error("Error saving donation")
            else:
                st.warning("Enter valid details ⚠️")
    else:
        st.info("View Only Mode 👁️")

    st.markdown("---")

    # ===== SHOW DATA =====
    try:
        data = supabase.table("donations").select("*").execute()
        df = pd.DataFrame(data.data)
    except:
        df = pd.DataFrame()

    st.dataframe(df)

    # ===== EDIT / DELETE =====
    if not df.empty:

        df["label"] = df["name"] + " | ₹" + df["amount"].astype(str) + " | " + df["date"]

        selected = st.selectbox("Select Donation", df["label"])

        row = df[df["label"] == selected].iloc[0]

        new_name = st.text_input("Edit Name", value=row["name"])
        new_amt = st.number_input("Edit Amount", value=float(row["amount"]))
        new_date = st.date_input("Edit Date", value=pd.to_datetime(row["date"]))

        col1, col2 = st.columns(2)

        # ===== UPDATE =====
        with col1:
            if not is_viewer:
                if st.button("Update Donation", key="update_donation"):
                    try:
                        supabase.table("donations").update({
                            "name": new_name,
                            "amount": new_amt,
                            "date": new_date.strftime("%Y-%m-%d")
                        }).eq("id", row["id"]).execute()

                        st.success("Updated ✅")
                        st.rerun()
                    except:
                        st.error("Update failed")

        # ===== DELETE =====
        with col2:
            if is_admin:
                if st.button("Delete Donation", key="delete_donation"):
                    try:
                        supabase.table("donations").delete().eq("id", row["id"]).execute()

                        st.warning("Deleted ⚠️")
                        st.rerun()
                    except:
                        st.error("Delete failed")
# ================= EXPENSES =================
elif menu == "Expenses":

    st.subheader("💸 Expense Management")

    # ===== ADD EXPENSE =====
    if not is_viewer:
        exp_type = st.text_input("Expense Type")
        date = st.date_input("Date")
        amt = st.number_input("Amount", min_value=0.0)

        if st.button("Save Expense", key="save_expense"):
            if exp_type and amt > 0:
                try:
                    supabase.table("expenses").insert({
                        "type": exp_type,
                        "amount": amt,
                        "date": date.strftime("%Y-%m-%d")
                    }).execute()

                    st.success("Expense Saved ✅")
                    st.rerun()
                except:
                    st.error("Error saving expense")
            else:
                st.warning("Enter valid details ⚠️")
    else:
        st.info("View Only Mode 👁️")

    st.markdown("---")

    # ===== SHOW DATA =====
    try:
        data = supabase.table("expenses").select("*").execute()
        df = pd.DataFrame(data.data)
    except:
        df = pd.DataFrame()

    st.dataframe(df)

    # ===== EDIT / DELETE =====
    if not df.empty:

        df["label"] = df["type"] + " | ₹" + df["amount"].astype(str) + " | " + df["date"]

        selected = st.selectbox("Select Expense", df["label"])

        row = df[df["label"] == selected].iloc[0]

        new_type = st.text_input("Edit Type", value=row["type"])
        new_amt = st.number_input("Edit Amount", value=float(row["amount"]))
        new_date = st.date_input("Edit Date", value=pd.to_datetime(row["date"]))

        col1, col2 = st.columns(2)

        # ===== UPDATE =====
        with col1:
            if not is_viewer:
                if st.button("Update Expense", key="update_expense"):
                    try:
                        supabase.table("expenses").update({
                            "type": new_type,
                            "amount": new_amt,
                            "date": new_date.strftime("%Y-%m-%d")
                        }).eq("id", row["id"]).execute()

                        st.success("Updated ✅")
                        st.rerun()
                    except:
                        st.error("Update failed")

        # ===== DELETE =====
        with col2:
            if is_admin:
                if st.button("Delete Expense", key="delete_expense"):
                    try:
                        supabase.table("expenses").delete().eq("id", row["id"]).execute()

                        st.warning("Deleted ⚠️")
                        st.rerun()
                    except:
                        st.error("Delete failed")
# ================= REPORT =================
elif menu == "Reports":

    st.subheader("📊 Advanced Reports")

    # LOAD COLLECTIONS
    try:
        data = supabase.table("collections").select("*").execute()
        df = pd.DataFrame(data.data)
    except:
        df = pd.DataFrame()

    if not df.empty:

        # ================= MONTH FILTER =================
        month_list = sorted(df["month"].unique())
        selected_month = st.selectbox("Select Month", month_list)

        df_month = df[df["month"] == selected_month]

        # ================= SUMMARY =================
        st.markdown("### 📅 Monthly Summary")

        total_collection = df_month["amount"].sum()

        # LOAD EXPENSES
        try:
            expense_df = pd.DataFrame(
                supabase.table("expenses").select("*").execute().data
            )
            total_expense = expense_df["amount"].sum() if not expense_df.empty else 0
        except:
            total_expense = 0

        # LOAD DONATIONS
        try:
            donation_df = pd.DataFrame(
                supabase.table("donations").select("*").execute().data
            )
            total_donation = donation_df["amount"].sum() if not donation_df.empty else 0
        except:
            total_donation = 0

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

        try:
            all_customers = pd.DataFrame(
                supabase.table("customers").select("*").execute().data
            )
        except:
            all_customers = pd.DataFrame()

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

    else:
        st.info("No collection data available yet")
# ================= USERS =================
if menu == "Users":

    st.subheader("👥 User Management")

    current_user = st.session_state.current_user
    role = st.session_state.role

    # ================= USER SELF PASSWORD CHANGE =================
    st.markdown("### 🔐 Change Your Password")

    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm New Password", type="password")

    if st.button("Update My Password"):

        try:
            user_data = supabase.table("users").select("*").eq("username", current_user).execute()

            if not user_data.data:
                st.error("User not found ❌")

            else:
                user = user_data.data[0]

                if hash_pass(old_pass) != user["password"]:
                    st.error("Old password incorrect ❌")

                elif new_pass != confirm_pass:
                    st.error("Passwords do not match ❌")

                elif len(new_pass) < 4:
                    st.error("Password too short ❌")

                else:
                    supabase.table("users").update({
                        "password": hash_pass(new_pass)
                    }).eq("username", current_user).execute()

                    st.success("Password updated successfully ✅")
                    st.rerun()

        except:
            st.error("Error updating password")

    st.markdown("---")

    # ================= ADMIN FEATURES =================
    if role == "Admin":

        # ===== CREATE USER =====
        st.markdown("### ➕ Create User")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        r = st.selectbox("Role", ["Admin","Editor","Viewer"])

        if st.button("Create User"):
            if u and p:
                try:
                    supabase.table("users").insert({
                        "username": u,
                        "password": hash_pass(p),
                        "role": r
                    }).execute()

                    st.success("User Created ✅")
                    st.rerun()
                except:
                    st.error("Error creating user")
            else:
                st.warning("Enter username & password")

        st.markdown("---")

        # ===== LOAD USERS =====
        try:
            users_df = pd.DataFrame(
                supabase.table("users").select("*").execute().data
            )
        except:
            users_df = pd.DataFrame()

        # ===== ADMIN RESET PASSWORD =====
        st.markdown("### 🔑 Reset User Password")

        if not users_df.empty:
            selected_user = st.selectbox("Select User", users_df["username"])
        else:
            selected_user = None

        new_pass_admin = st.text_input("New Password for User", type="password")

        if st.button("Reset Password"):
            if selected_user and new_pass_admin:
                try:
                    supabase.table("users").update({
                        "password": hash_pass(new_pass_admin)
                    }).eq("username", selected_user).execute()

                    st.success("Password Reset Done ✅")
                    st.rerun()
                except:
                    st.error("Reset failed")
            else:
                st.warning("Enter new password")

        st.markdown("---")

        # ===== DELETE USER =====
        st.markdown("### 🗑️ Delete User")

        if not users_df.empty:
            del_user = st.selectbox("Select User to Delete", users_df["username"])
        else:
            del_user = None

        if st.button("Delete User"):
            if del_user == "admin":
                st.error("Admin cannot be deleted ❌")
            elif del_user:
                try:
                    supabase.table("users").delete().eq("username", del_user).execute()

                    st.warning("User Deleted ⚠️")
                    st.rerun()
                except:
                    st.error("Delete failed")

        st.markdown("---")

        # ===== SHOW USERS =====
        st.markdown("### 📋 All Users")

        if not users_df.empty:
            st.dataframe(users_df[["username", "role"]])
        else:
            st.info("No users found")

    else:
        st.info("Limited access: You can only change your password 👁️")

# ================= AI =================
elif menu == "AI":
    st.subheader("🤖 AI Insights (Coming Soon)")
    st.info("Future AI features yaha add honge")

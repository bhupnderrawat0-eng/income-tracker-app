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

/* ===== ANIMATED BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a,#020617);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

/* ===== HIDE HEADER ===== */
header, footer {visibility:hidden;}
.block-container {padding-top:1rem;}

/* ===== TEXT ===== */
h1,h2,h3,h4,h5,p,label {
    color:white !important;
}

/* ===== SIDEBAR GLASS ===== */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ===== GLASS CARD ===== */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(18px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
    transition: all 0.25s ease;
}

/* ===== CARD HOVER (soft) ===== */
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(124,58,237,0.25);
}

/* ===== INPUT FIELDS ===== */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background: rgba(17,24,39,0.75) !important;
    color:white !important;
    border-radius:10px !important;
    border:1px solid rgba(255,255,255,0.08);
}

/* ===== SELECTBOX FIX ===== */
.stSelectbox div[data-baseweb="select"] {
    background: rgba(17,24,39,0.75) !important;
    border-radius:10px !important;
    border:1px solid rgba(255,255,255,0.08);
}

/* ===== BUTTONS ===== */
div.stButton > button {
    background: linear-gradient(135deg,#6366f1,#7c3aed);
    color: white;
    border-radius: 12px;
    height: 42px;
    border: none;
    transition: all 0.25s ease;
}

/* ===== BUTTON HOVER (controlled) ===== */
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 12px rgba(124,58,237,0.4);
}

/* ===== FORM BUTTON (LOGIN SAFE) ===== */
div.stForm button {
    background: linear-gradient(135deg,#16a34a,#22c55e) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: all 0.25s ease;
}

div.stForm button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 10px rgba(34,197,94,0.5);
}

/* ===== METRIC CARDS ===== */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(18px);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.25s ease;
}

/* ===== METRIC HOVER ===== */
[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 15px rgba(124,58,237,0.3);
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 5px;
}

/* ===== CHART AREA ===== */
canvas {
    background: rgba(255,255,255,0.02) !important;
    border-radius: 10px;
}

/* ===== FADE ANIMATION ===== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeInUp 0.5s ease forwards;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
}

/* ===== MOBILE FIX ===== */
html, body, .stApp {
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .block-container {
        padding: 10px !important;
    }

    div.stButton > button {
        width: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)
# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
import time

SESSION_TIMEOUT = 1800  # 30 minutes

# ===== CHECK SESSION TIMEOUT =====
if st.session_state.get("logged_in"):

    if "last_active" not in st.session_state:
        st.session_state.last_active = time.time()

    if time.time() - st.session_state.last_active > SESSION_TIMEOUT:
        st.warning("Session expired. Please login again.")
        st.session_state.clear()
        st.rerun()

    # update activity time
    st.session_state.last_active = time.time()


# ===== LOGIN SYSTEM =====
if not st.session_state.get("logged_in", False):

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

                            # ✅ SESSION SET
                            st.session_state.logged_in = True
                            st.session_state.current_user = user["username"]
                            st.session_state.role = user["role"]

                            # ✅ START TIMER
                            st.session_state.last_active = time.time()

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
    menu_list = ["Dashboard","Members","Collections","loans","Donations","Expenses","Reports","Users","AI"]
elif is_editor:
    menu_list = ["Dashboard","Members","Collections","loans","Donations","Expenses","Reports"]
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
    st.write(f"👤 {st.session_state.get('current_user','User')}")

with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("---")


# ================= HEADER =================
col1, col2 = st.columns([4,1])

with col1:
    st.markdown("""
    ### 🚀 Bal Yuva Mangal Dal
    <p style='color:lightgray;'>Smart Finance SaaS System</p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <p style='text-align:right; color:#94a3b8; margin-top:20px;'>
    Welcome, {st.session_state.get("current_user","User")}
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")
# ================= DASHBOARD =================
if menu == "Dashboard":

    import plotly.express as px

    # ✅ CACHE FUNCTION (BIG SPEED BOOST)
    @st.cache_data(ttl=60)
    def get_sum_cached(table_name):
        try:
            data = supabase.table(table_name).select("amount").execute()
            if data.data:
                return sum(item["amount"] for item in data.data)
            return 0
        except:
            return 0

    @st.cache_data(ttl=60)
    def get_collection_data():
        try:
            return supabase.table("collections").select("amount,date").execute().data
        except:
            return []

    # ✅ FAST SUM (no pandas)
    total_col = get_sum_cached("collections")
    total_loan = get_sum_cached("loans")
    total_don = get_sum_cached("donations")
    total_exp = get_sum_cached("expenses")

    # ===== METRICS =====
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Collections", f"₹ {total_col}")
    c2.metric("Loans", f"₹ {total_loan}")
    c3.metric("Donations", f"₹ {total_don}")
    c4.metric("Expenses", f"₹ {total_exp}")

    st.metric("Balance", f"₹ {total_col + total_don - total_exp}")

    st.markdown("---")

    # ===== COLLECTION TREND CHART =====
    st.markdown("### 📊 Collection Trend")

    try:
        data = get_collection_data()

        if data:
            df = pd.DataFrame(data)

            df["date"] = pd.to_datetime(df["date"])

            fig = px.line(
                df,
                x="date",
                y="amount",
                title="Collection Growth",
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No collection data available")

    except Exception as e:
        st.error(f"Chart Error: {e}")
# ========================= MEMBERS =========================
elif menu == "Members":

    import uuid

    st.subheader("👤 Member Management")

    name = st.text_input("Member Name")
    mobile = st.text_input("Mobile")
    start_date = st.date_input("Start Date")
    notes = st.text_area("Notes")

    # ================= ADD MEMBER =================

    if st.button("Add Member"):

        if not name.strip():
            st.warning("Please enter member name")
            st.stop()

        try:

            unique_id = str(uuid.uuid4())

            customer_id = "MEM-" + unique_id[:6].upper()

            supabase.table("members").insert({
                "id": unique_id,
                "customer_id": customer_id,
                "name": name.strip(),
                "mobile": mobile.strip(),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "notes": notes.strip()
            }).execute()

            st.success(f"Member Added ✅ ({customer_id})")

            st.cache_data.clear()
            st.rerun()

        except Exception as e:
            st.error(f"Error adding member: {e}")

    # ================= CACHE DATA =================

    @st.cache_data(ttl=60)
    def load_members():
        try:
            return supabase.table("members").select("*").execute().data
        except:
            return []

    data = load_members()
    df = pd.DataFrame(data)

    # ================= SHOW DATA =================

    if not df.empty:

        show_columns = [
            col for col in [
                "customer_id",
                "name",
                "mobile",
                "start_date",
                "notes"
            ]
            if col in df.columns
        ]

        st.dataframe(
            df[show_columns],
            use_container_width=True
        )

        # ================= SELECT MEMBER =================

        member_options = {
            f"{row.get('customer_id', 'NO-ID')} | {row['name']}": row["id"]
            for _, row in df.iterrows()
        }

        selected_member = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        selected_id = member_options[selected_member]

        row = df[df["id"] == selected_id].iloc[0]

        # ================= EDIT SECTION =================

        new_name = st.text_input(
            "Edit Name",
            value=row["name"]
        )

        new_mobile = st.text_input(
            "Edit Mobile",
            value=row["mobile"]
        )

        new_start = st.date_input(
            "Edit Start Date",
            value=pd.to_datetime(row["start_date"])
        )

        new_notes = st.text_area(
            "Edit Notes",
            value=row.get("notes", "")
        )

        col1, col2 = st.columns(2)

        # ================= UPDATE =================

        with col1:

            if st.button("Update Member"):

                try:

                    supabase.table("members").update({
                        "name": new_name.strip(),
                        "mobile": new_mobile.strip(),
                        "start_date": new_start.strftime("%Y-%m-%d"),
                        "notes": new_notes.strip()
                    }).eq("id", selected_id).execute()

                    st.success("Updated ✅")

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Update failed: {e}")

        # ================= DELETE =================

        with col2:

            if st.button("Delete Member"):

                try:

                    supabase.table("members").delete().eq(
                        "id",
                        selected_id
                    ).execute()

                    st.warning("Deleted ⚠️")

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Delete failed: {e}")
# ========================= COLLECTION =========================
elif menu == "Collections":

    st.subheader("🔥 Collection Management")

    # ================= LOAD MEMBERS =================

    @st.cache_data(ttl=60)
    def load_members():
        try:
            return supabase.table("members").select("*").execute().data
        except:
            return []

    # ================= LOAD COLLECTIONS =================

    @st.cache_data(ttl=60)
    def load_collections():
        try:
            return supabase.table("collections").select("*").execute().data
        except:
            return []

    members_data = load_members()
    members_df = pd.DataFrame(members_data)

    # ================= MEMBER SELECTION =================

    if members_df.empty:

        st.warning("No members available")

    else:

        member_options = {
            f"{row.get('customer_id', 'NO-ID')} | {row['name']}": row
            for _, row in members_df.iterrows()
        }

        selected_member = st.selectbox(
            "Member",
            list(member_options.keys())
        )

        member_row = member_options[selected_member]

        member_name = member_row["name"]
        member_id = member_row["id"]
        customer_id = member_row.get("customer_id", "")
        start_date = member_row.get("start_date", "")

        # ================= FORM =================

        month = st.selectbox(
            "Month",
            [datetime.date(2026, m, 1).strftime("%B %Y") for m in range(1, 13)]
        )

        payment_date = st.date_input("Payment Date")

        amt = st.number_input("Amount")

        note = st.text_input(
            "📝 Note / Comment",
            key="collection_note"
        )

        # ================= SAVE =================

        if not is_viewer:

            if st.button("Save Collection"):

                try:

                    supabase.table("collections").insert({

                        "member_id": member_id,
                        "customer_id": customer_id,
                        "name": member_name,
                        "month": month,
                        "start_date": start_date,
                        "date": payment_date.strftime("%Y-%m-%d"),
                        "amount": amt,
                        "note": note

                    }).execute()

                    st.success("Collection Saved ✅")

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error saving collection: {e}")

    # ================= LOAD DATA =================

    data = load_collections()
    df = pd.DataFrame(data)

    # ================= SHOW DATA =================

    if not df.empty:

        show_columns = [
            col for col in [
                "customer_id",
                "name",
                "month",
                "amount",
                "date",
                "note"
            ]
            if col in df.columns
        ]

        st.dataframe(
            df[show_columns],
            use_container_width=True
        )

        # ================= SELECT ENTRY =================

        df["label"] = (
            df["customer_id"].fillna("NO-ID")
            + " | "
            + df["name"]
            + " | "
            + df["month"]
            + " | ₹"
            + df["amount"].astype(str)
        )

        selected = st.selectbox(
            "Select Entry",
            df["label"]
        )

        row = df[df["label"] == selected].iloc[0]

        new_amt = st.number_input(
            "Edit Amount",
            value=float(row["amount"])
        )

        new_note = st.text_input(
            "Edit Note",
            value=row.get("note", "")
        )

        col1, col2 = st.columns(2)

        # ================= UPDATE =================

        with col1:

            if not is_viewer:

                if st.button("Update Collection"):

                    try:

                        supabase.table("collections").update({

                            "amount": new_amt,
                            "note": new_note

                        }).eq("id", row["id"]).execute()

                        st.success("Updated ✅")

                        st.cache_data.clear()
                        st.rerun()

                    except Exception as e:
                        st.error(f"Update failed: {e}")

        # ================= DELETE =================

        with col2:

            if is_admin:

                if st.button("Delete Collection"):

                    try:

                        supabase.table("collections").delete().eq(
                            "id",
                            row["id"]
                        ).execute()

                        st.warning("Deleted ⚠️")

                        st.cache_data.clear()
                        st.rerun()

                    except Exception as e:
                        st.error(f"Delete failed: {e}")
# ========================= LOANS =========================
elif menu == "loans":

    from datetime import datetime

    st.subheader("💰 Loan Management")

    # ================= LOAD DATA =================

    @st.cache_data(ttl=60)
    def load_all_data():

        try:
            members = supabase.table("members").select("*").execute().data
        except:
            members = []

        try:
            loans = supabase.table("loans").select("*").execute().data
        except:
            loans = []

        try:
            payments = supabase.table("loan_payments").select("*").execute().data
        except:
            payments = []

        return members, loans, payments

    members_data, loans_data, payments_data = load_all_data()

    members_df = pd.DataFrame(members_data)
    loans_df = pd.DataFrame(loans_data)
    payments_df = pd.DataFrame(payments_data)

    # ================= ADD LOAN =================

    st.markdown("### ➕ Add Loan")

    if members_df.empty:

        st.warning("No members found")

    else:

        member_options = {

            f"{row.get('customer_id', 'NO-ID')} | {row['name']}": row

            for _, row in members_df.iterrows()
        }

        selected_member = st.selectbox(
            "Member",
            list(member_options.keys())
        )

        member_row = member_options[selected_member]

        cust = member_row["name"]
        member_id = member_row["id"]
        customer_id = member_row.get("customer_id", "")

        loan_amt = st.number_input(
            "Loan Amount",
            min_value=0.0
        )

        interest_rate = st.number_input(
            "Interest % per month",
            value=1.0
        )

        loan_date = st.date_input(
            "Loan Start Date"
        )

        note = st.text_input(
            "📝 Note / Comment",
            key="loan_note"
        )

        # ================= SAVE LOAN =================

        if not is_viewer:

            if st.button(
                "Add Loan",
                key="add_loan_btn"
            ):

                try:

                    supabase.table("loans").insert({

                        "customer_name": cust,
                        "member_id": member_id,
                        "customer_id": customer_id,
                        "amount": loan_amt,
                        "interest_rate": interest_rate,
                        "start_date": loan_date.strftime("%Y-%m-%d"),
                        "note": note

                    }).execute()

                    st.success("Loan Added ✅")

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:

                    st.error(f"Error adding loan: {e}")

    st.markdown("---")

    # ================= SHOW LOANS =================

    if not loans_df.empty:

        st.markdown("📌 Existing Loans")

        for _, row in loans_df.iterrows():

            st.write(

                f"{row.get('customer_id', 'NO-ID')} | "
                f"{row.get('customer_name', 'Unknown')} | "
                f"₹{row.get('amount', 0)}"

            )

    # ================= NO LOANS =================

    if loans_df.empty:

        st.info("No loans available")
        st.stop()

    # ================= LABEL =================

    loans_df["label"] = loans_df.apply(

        lambda x:

        f"{x.get('customer_id', 'NO-ID')} | "
        f"{x.get('customer_name', 'Unknown')} | "
        f"Loan #{x['id']} | "
        f"₹{x.get('amount', 0)}",

        axis=1
    )

    selected = st.selectbox(
        "Select Loan",
        loans_df["label"]
    )

    selected_row = loans_df[
        loans_df["label"] == selected
    ]

    if selected_row.empty:

        st.error("Loan not found")
        st.stop()

    loan = selected_row.iloc[0]

    loan_id = int(loan["id"])

    # ================= ADD PAYMENT =================

    st.markdown("### ➕ Add Payment")

    if not is_viewer:

        pay_amt = st.number_input(
            "Payment Amount",
            min_value=0.0
        )

        pay_date = st.date_input(
            "Payment Date"
        )

        pay_note = st.text_input(
            "📝 Payment Note",
            key="loan_payment_note"
        )

        if st.button(
            "Add Payment",
            key="add_payment_btn"
        ):

            if pay_amt > 0:

                try:

                    supabase.table("loan_payments").insert({

                        "loan_id": loan_id,
                        "amount": pay_amt,
                        "date": pay_date.strftime("%Y-%m-%d"),
                        "note": pay_note

                    }).execute()

                    st.success("Payment Added ✅")

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:

                    st.error(f"Error adding payment: {e}")

    # ================= SAFE PAYMENTS =================

    if payments_df.empty or "loan_id" not in payments_df.columns:

        cust_payments = pd.DataFrame()

    else:

        cust_payments = payments_df[

            payments_df["loan_id"] == loan_id

        ].sort_values("date")

    # ================= CALCULATIONS =================

    principal = float(loan.get("amount", 0))

    rate = float(loan.get("interest_rate", 0))

    total_paid = (

        cust_payments["amount"].sum()

        if not cust_payments.empty

        else 0

    )

    start_date = loan.get("start_date")

    if isinstance(start_date, str):

        start_date = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

    today = datetime.today()

    payment_map = {}

    if not cust_payments.empty:

        for _, p in cust_payments.iterrows():

            key = str(p["date"])[:7]

            payment_map[key] = (

                payment_map.get(key, 0)

                + p["amount"]

            )

    timeline = []

    current_date = start_date

    # ✅ running balance
    running_principal = principal

    while current_date <= today:

        month_str = current_date.strftime("%Y-%m")

        # ✅ current month payment
        payment = payment_map.get(
            month_str,
            0
        )

        # ✅ payment first reduce hoga
        principal_after_payment = max(
            running_principal - payment,
            0
        )

        # ✅ interest remaining balance pe lagega
        interest = (
            principal_after_payment * rate
        ) / 100

        # ✅ final balance
        balance_after = (
            principal_after_payment + interest
        )

        timeline.append({

            "Month": current_date.strftime("%b %Y"),

            "Principal": round(
                principal_after_payment,
                2
            ),

            "Interest": round(
                interest,
                2
            ),

            "Payment": payment,

            "Balance": round(
                balance_after,
                2
            )

        })

        # ✅ next month carry
        running_principal = balance_after

        # ================= NEXT MONTH =================

        if current_date.month == 12:

            current_date = current_date.replace(

                year=current_date.year + 1,
                month=1

            )

        else:

            current_date = current_date.replace(

                month=current_date.month + 1

            )

    # ================= FINAL TOTALS =================

    total_interest = sum(

        x["Interest"]

        for x in timeline

    )

    balance = (

        timeline[-1]["Balance"]

        if timeline

        else principal

    )

    # ================= SUMMARY =================

    st.markdown("### 📊 Loan Summary")

    st.write(f"Principal: ₹{principal}")

    st.write(f"Total Paid: ₹{total_paid}")

    st.write(
        f"Total Interest: ₹{round(total_interest, 2)}"
    )

    st.write(
        f"Balance: ₹{round(balance, 2)}"
    )

    # ================= TIMELINE =================

    st.markdown("### 📅 Monthly Breakdown")

    timeline_df = pd.DataFrame(timeline)

    st.dataframe(
        timeline_df,
        use_container_width=True
    )

    # ================= DELETE =================

    st.markdown("---")

    if is_admin:

        if st.button(
            "Delete Loan",
            key="delete_loan_btn"
        ):

            try:

                supabase.table("loans").delete().eq(
                    "id",
                    loan_id
                ).execute()

                supabase.table("loan_payments").delete().eq(
                    "loan_id",
                    loan_id
                ).execute()

                st.success("Loan Deleted 🗑️")

                st.cache_data.clear()
                st.rerun()

            except Exception as e:

                st.error(f"Delete failed: {e}")
# ================= DONATIONS =================
elif menu == "Donations":

    st.subheader("🎁 Donations Management")

    # ✅ CACHE DATA
    @st.cache_data(ttl=60)
    def load_donations():
        try:
            return supabase.table("donations").select("*").execute().data
        except:
            return []

    # ===== ADD DONATION =====
    if not is_viewer:
        donor = st.text_input("Donor Name")
        date = st.date_input("Date")
        amt = st.number_input("Amount", min_value=0.0)

        # ✅ NOTE FIELD ADDED
        note = st.text_input("📝 Note / Comment", key="donation_note")

        if st.button("Save Donation", key="save_donation"):
            if donor and amt > 0:
                try:
                    supabase.table("donations").insert({
                        "name": donor,
                        "amount": amt,
                        "date": date.strftime("%Y-%m-%d"),
                        "note": note   # ✅ added
                    }).execute()

                    st.success("Donation Saved ✅")

                    st.cache_data.clear()
                    st.rerun()

                except:
                    st.error("Error saving donation")
            else:
                st.warning("Enter valid details ⚠️")
    else:
        st.info("View Only Mode 👁️")

    st.markdown("---")

    # ===== SHOW DATA =====
    data = load_donations()
    df = pd.DataFrame(data)

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

                        st.cache_data.clear()
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

                        st.cache_data.clear()
                        st.rerun()

                    except:
                        st.error("Delete failed")
# ================= EXPENSES =================
elif menu == "Expenses":

    st.subheader("💸 Expense Management")

    # ✅ CACHE DATA
    @st.cache_data(ttl=60)
    def load_expenses():
        try:
            return supabase.table("expenses").select("*").execute().data
        except:
            return []

    # ===== ADD EXPENSE =====
    if not is_viewer:
        exp_type = st.text_input("Expense Type")
        date = st.date_input("Date")
        amt = st.number_input("Amount", min_value=0.0)

        # ✅ NOTE FIELD ADDED
        note = st.text_input("📝 Note / Comment", key="expense_note")

        if st.button("Save Expense", key="save_expense"):
            if exp_type and amt > 0:
                try:
                    supabase.table("expenses").insert({
                        "type": exp_type,
                        "amount": amt,
                        "date": date.strftime("%Y-%m-%d"),
                        "note": note   # ✅ added
                    }).execute()

                    st.success("Expense Saved ✅")

                    st.cache_data.clear()
                    st.rerun()

                except:
                    st.error("Error saving expense")
            else:
                st.warning("Enter valid details ⚠️")
    else:
        st.info("View Only Mode 👁️")

    st.markdown("---")

    # ===== SHOW DATA =====
    data = load_expenses()
    df = pd.DataFrame(data)

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

                        st.cache_data.clear()
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

                        st.cache_data.clear()
                        st.rerun()

                    except:
                        st.error("Delete failed")
# ================= REPORT =================
elif menu == "Reports":

    st.subheader("📊 Advanced Reports")

    @st.cache_data(ttl=60)
    def load_all_reports_data():
        try:
            collections = supabase.table("collections").select("*").execute().data
        except:
            collections = []

        try:
            expenses = supabase.table("expenses").select("*").execute().data
        except:
            expenses = []

        try:
            donations = supabase.table("donations").select("*").execute().data
        except:
            donations = []

        try:
            customers = supabase.table("customers").select("*").execute().data
        except:
            customers = []

        try:
            loans = supabase.table("loans").select("*").execute().data
        except:
            loans = []

        try:
            payments = supabase.table("loan_payments").select("*").execute().data
        except:
            payments = []

        return collections, expenses, donations, customers, loans, payments

    collections_data, expenses_data, donations_data, customers_data, loans_data, payments_data = load_all_reports_data()

    # 🔒 ORIGINAL DATA SAFE
    df_original = pd.DataFrame(collections_data)

    df = df_original.copy()
    expense_df = pd.DataFrame(expenses_data)
    donation_df = pd.DataFrame(donations_data)
    all_customers = pd.DataFrame(customers_data)
    loans_df = pd.DataFrame(loans_data)
    payments_df = pd.DataFrame(payments_data)

    # ================= DATE FILTER =================
    st.markdown("### 📅 Date Filter")
    from_date = st.date_input("From Date")
    to_date = st.date_input("To Date")

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df = df[(df["date"] >= pd.to_datetime(from_date)) & (df["date"] <= pd.to_datetime(to_date))]

    if not df.empty:

        # ================= MONTH FILTER =================
        month_list = sorted(df_original["month"].unique())
        selected_month = st.selectbox("Select Month", month_list)

        df_month = df[df["month"] == selected_month]

        # ================= SUMMARY =================
        st.markdown("### 📅 Monthly Summary")

        total_collection = df_month["amount"].sum()
        total_expense = expense_df["amount"].sum() if not expense_df.empty else 0
        total_donation = donation_df["amount"].sum() if not donation_df.empty else 0

        balance = total_collection + total_donation - total_expense

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Collection", f"₹ {total_collection}")
        c2.metric("Donations", f"₹ {total_donation}")
        c3.metric("Expenses", f"₹ {total_expense}")
        c4.metric("Balance", f"₹ {balance}")

        # ================= CUSTOMER REPORT =================
        st.markdown("### 👤 Customer-wise Report")
        customer_summary = df_month.groupby("name")["amount"].sum().reset_index()
        st.dataframe(customer_summary)

        # ================= LOAN REPORT =================
        st.markdown("### 💰 Loan Report")

        if not loans_df.empty:
            report = []
            for _, loan in loans_df.iterrows():
                loan_id = loan["id"]
                principal = loan["amount"]
                rate = loan["interest_rate"]

                loan_payments = payments_df[payments_df["loan_id"] == loan_id]
                paid = loan_payments["amount"].sum() if not loan_payments.empty else 0

                interest = (principal * rate) / 100
                balance_loan = principal + interest - paid

                report.append({
                    "Member": loan["customer_name"],
                    "Principal": principal,
                    "Interest": round(interest,2),
                    "Paid": paid,
                    "Balance": round(balance_loan,2),
                    "Note": loan.get("note","")
                })

            st.dataframe(pd.DataFrame(report))

        # ================= DONATION REPORT =================
        st.markdown("### 🎁 Donation Report")
        st.dataframe(donation_df)

        # ================= EXPENSE REPORT =================
        st.markdown("### 💸 Expense Report")
        st.dataframe(expense_df)

        # ================= 🔔 SMART REMINDER SYSTEM =================
        st.markdown("### 🔔 Smart Reminder System")

        paid_customers = df_original[df_original["month"] == selected_month]["name"].unique()

        pending_list = all_customers[
            ~all_customers["name"].isin(paid_customers)
        ]

        total_pending = len(pending_list)

        if not pending_list.empty:

            st.warning(f"Pending Members: {total_pending}")
            st.dataframe(pending_list)

        else:
            st.success("✅ All customers have paid for this month")

        # ================= ⚠️ RISK =================
        st.markdown("### ⚠️ Risk Analysis")

        try:
            all_months = df_original["month"].unique()

            risk_data = []

            for cust in all_customers["name"]:
                paid_months = df_original[df_original["name"] == cust]["month"].unique()
                missed = len(set(all_months) - set(paid_months))

                risk_data.append({
                    "Customer": cust,
                    "Missed Months": missed
                })

            st.dataframe(pd.DataFrame(risk_data))

        except:
            pass

        # ================= DOWNLOAD =================
        st.markdown("### 📥 Download")

        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        st.download_button("Download Collections", convert_df(df_month), "collections.csv")

    else:
        st.info("No collection data available yet")
# ================= USERS =================
if menu == "Users":

    st.subheader("👥 User Management")

    current_user = st.session_state.current_user
    role = st.session_state.role

    # ✅ CACHE USERS DATA
    @st.cache_data(ttl=60)
    def load_users():
        try:
            return supabase.table("users").select("*").execute().data
        except:
            return []

    users_data = load_users()
    users_df = pd.DataFrame(users_data)

    # ================= USER SELF PASSWORD CHANGE =================
    st.markdown("### 🔐 Change Your Password")

    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm New Password", type="password")

    if st.button("Update My Password"):
        try:
            user_row = users_df[users_df["username"] == current_user]

            if user_row.empty:
                st.error("User not found ❌")

            else:
                user = user_row.iloc[0]

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
                    st.cache_data.clear()
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
        r = st.selectbox("Role", ["Admin", "Editor", "Viewer"])

        if st.button("Create User"):
            if u and p:
                try:
                    username = u.strip().lower()

                    existing = supabase.table("users") \
                        .select("username") \
                        .eq("username", username) \
                        .execute()

                    if existing.data:
                        st.warning("⚠️ Username already exists")
                    else:
                        supabase.table("users").insert({
                            "username": username,
                            "password": hash_pass(p),
                            "role": r
                        }).execute()

                        st.success("User Created ✅")
                        st.cache_data.clear()
                        st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

            else:
                st.warning("Enter username & password")

        st.markdown("---")

        # ===== RESET PASSWORD =====
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
                    st.cache_data.clear()
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
                    st.cache_data.clear()
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

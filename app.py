import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import hashlib
import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Bal Yuva Mangal Dal", layout="wide")

# =========================
# SESSION STATE
# =========================
if "customers" not in st.session_state:
    st.session_state.customers = []

if "collections" not in st.session_state:
    st.session_state.collections = []

# =========================
# SIDEBAR MENU
# =========================
with st.sidebar:
    menu = option_menu(
        menu_title=None,
        options=["Dashboard", "Customers", "Collections"],
        icons=["grid", "people", "cash"],
        default_index=0
    )

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.title("📊 Dashboard")

    total = sum(x["amount"] for x in st.session_state.collections)

    st.metric("Total Collections", f"₹ {total}")

# =========================
# CUSTOMERS
# =========================
elif menu == "Customers":

    st.title("👥 Customers")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Customer Name")

    with col2:
        mobile = st.text_input("Mobile")

    with col3:
        date = st.date_input("Meeting Date")

    if st.button("Add Customer"):
        if name and mobile:
            st.session_state.customers.append({
                "name": name,
                "mobile": mobile,
                "date": str(date)
            })
            st.success("Added")
        else:
            st.error("Fill all fields")

    if len(st.session_state.customers) > 0:
        df = pd.DataFrame(st.session_state.customers)
        st.dataframe(df, use_container_width=True)

# =========================
# COLLECTIONS
# =========================
elif menu == "Collections":

    st.title("💵 Collections")

    if len(st.session_state.customers) == 0:
        st.warning("Add customers first")

    else:
        customer = st.selectbox(
            "Select Customer",
            st.session_state.customers,
            format_func=lambda x: f"{x['name']} ({x['mobile']})"
        )

        current_month = datetime.datetime.now().strftime("%B %Y")

        month = st.selectbox(
            "Month",
            [current_month, "January 2026", "February 2026", "March 2026"]
        )

        amount = st.number_input("Amount", min_value=0.0)

        if st.button("Save"):
            st.session_state.collections.append({
                "name": customer["name"],
                "mobile": customer["mobile"],
                "month": month,
                "amount": amount
            })
            st.success("Saved")

    if len(st.session_state.collections) > 0:
        df = pd.DataFrame(st.session_state.collections)

        selected_month = st.selectbox(
            "Filter",
            ["All"] + list(df["month"].unique())
        )

        if selected_month != "All":
            df = df[df["month"] == selected_month]

        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data")

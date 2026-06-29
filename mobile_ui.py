import streamlit as st
from streamlit_option_menu import option_menu

# ================= DEVICE DETECTION =================
def is_mobile():
    user_agent = st.context.headers.get(
        "user-agent",
        ""
    ).lower()
    return (
        "android" in user_agent
        or "iphone" in user_agent
    )


# ================= MOBILE CSS =================
def load_mobile_css():
    st.markdown(
        """
        <style>
        @media (max-width:768px){
            .block-container{
                padding:12px !important;
                padding-bottom: 100px !important; /* TAकी MAIN CONTENT NAVIGATION BAR KE PICHE NA CHUPE */
            }
            h1{
                font-size:30px !important;
            }
            h2{
                font-size:24px !important;
            }
            h3{
                font-size:20px !important;
            }
            p{
                font-size:14px !important;
            }
            div.stButton > button{
                width:100% !important;
                min-height:48px !important;
                border-radius:12px !important;
            }
            [data-testid="metric-container"]{
                padding:12px !important;
            }
        }
        .section-title{
            color:#F8D568;
            font-size:18px;
            font-weight:600;
            margin-top:20px;
            margin-bottom:12px;
        }

        /* FIXED BOTTOM NAVIGATION CSS */
        .stElementContainer:has(.bottom-nav-container) {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100% !important;
            background-color: #0E1117 !important; /* Streamlit default dark background - isko aap change kar sakte hain */
            padding: 10px 15px 20px 15px !important;
            z-index: 999999 !important;
            box-shadow: 0px -4px 10px rgba(0,0,0,0.5);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ================= MOBILE HEADER =================
def show_mobile_header():
    st.image(
        "logo.png",
        width=120
    )
    st.markdown(
        """
        <h3 style="
            text-align:center;
            color:#F8D568;
        ">
            बाल युवा मंगलदल समिति
        </h3>
        """,
        unsafe_allow_html=True
    )


# ================= MOBILE TOP BAR =================
def show_mobile_topbar(username):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "logo.png",
            width=120
        )
    st.markdown(
        """
        <h2 style="
            text-align:center;
            color:#F8D568;
            margin-top:-10px;
            margin-bottom:5px;
            font-size:34px;
        ">
            बाल युवा मंगलदल समिति
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <p style="
            text-align:center;
            color:#CBD5E1;
            font-size:20px;
            margin-top:0px;
            margin-bottom:25px;
        ">
            👋 Welcome, {username}
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)


# ================= MOBILE SECTION TITLE =================
def show_mobile_section_title(title):
    st.markdown(
        f"""
        <div class="section-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


# ================= METRIC COLUMNS =================
def get_metric_columns():
    if is_mobile():
        row1 = st.columns(2)
        row2 = st.columns(2)
        return row1, row2
    else:
        return st.columns(4)


# ================= MOBILE METRIC CARD =================
def show_mobile_metric_card(title, value):
    import streamlit.components.v1 as components
    html_content = f"""
    <div style="
        background: rgba(255,255,255,0.05); 
        border: 1px solid rgba(255,255,255,0.08); 
        border-radius: 18px; 
        padding: 18px; 
        font-family: sans-serif;
        text-align: center;
    ">
        <div style="color: #cbd5e1; font-size: 15px; margin-bottom: 12px;">
            {title}
        </div>
        <div style="color: white; font-size: 26px; font-weight: 700;">
            {value}
        </div>
    </div>
    """
    components.html(html_content, height=110, scrolling=False)


# ================= MOBILE NAVIGATION =================
def show_mobile_navigation():
    # Invisible marker div jo CSS anchor ke liye use hoga aur buttons ko screen ke niche bhej dega
    st.markdown('<div class="bottom-nav-container"></div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("🏠", use_container_width=True):
        st.session_state.mobile_menu = "Dashboard"

    if col2.button("👥", use_container_width=True):
        st.session_state.mobile_menu = "Members"

    if col3.button("💰", use_container_width=True):
        st.session_state.mobile_menu = "Collections"

    if col4.button("📊", use_container_width=True):
        st.session_state.mobile_menu = "Reports"

    if col5.button("☰", use_container_width=True):
        st.session_state.show_more = (
            not st.session_state.get("show_more", False)
        )

    if st.session_state.get("show_more", False):
        more_menu = st.selectbox(
            "More",
            [
                "Loans",
                "Donations",
                "Expenses"
            ]
        )
        st.session_state.mobile_menu = more_menu

    return st.session_state.get(
        "mobile_menu",
        "Dashboard"
    )

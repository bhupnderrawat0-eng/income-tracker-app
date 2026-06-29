import streamlit as st
from streamlit_option_menu import option_menu


# ================= DEVICE DETECTION =================
def is_mobile():
    user_agent = st.context.headers.get("user-agent", "").lower()
    return "android" in user_agent or "iphone" in user_agent


# ================= MOBILE CSS =================
def load_mobile_css():
    st.markdown(
        """
        <style>
        @media (max-width:768px){
            .block-container{
                padding:12px !important;
                padding-bottom: 120px !important; /* Content takki navbar ke piche na chupe */
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

        /* Pure HTML Custom Navbar Styling */
        .custom-bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #111424; /* Aapke app ka background color */
            padding: 12px 0px 25px 0px;
            z-index: 999999;
            box-shadow: 0px -5px 15px rgba(0,0,0,0.6);
            border-top: 1px solid rgba(255,255,255,0.08);
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
        
        .nav-btn {
            width: 18%;
            height: 50px;
            font-size: 22px;
            border-radius: 14px;
            border: none;
            background: #5856D6; /* Purple color jo aapko chahiye */
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }
        
        .nav-btn:active {
            background: #403ebd;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ================= MOBILE HEADER =================
def show_mobile_header():
    st.image("logo.png", width=120)
    st.markdown(
        """
        <h3 style="
            text-align:center;
            color:#F8D568;
        ">
            बाल युवा मंगलदल समिति
        </h3>
        """,
        unsafe_allow_html=True,
    )


# ================= MOBILE TOP BAR =================
def show_mobile_topbar(username):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=120)
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
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
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
    # Streamlit ka official container jo elements ko page ke bottom mein bhej deta hai
    with st.bottom():
        # Custom spacing ke liye styling injection
        st.markdown(
            """
            <style>
            /* Sabhi buttons ko ek barabar aur ek hi line (horizontal) mein force karne ke liye */
            div[data-testid="stBottom"] div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                justify-content: space-between !important;
                background-color: #111424 !important; /* Aapka background */
                padding: 10px !important;
                border-radius: 15px;
            }
            div[data-testid="stBottom"] div[data-testid="column"] {
                width: 19% !important;
                flex: unset !important;
                min-width: unset !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        # Ab ye pure native buttons hain, inpar click hote ही Streamlit screen update kar dega
        if col1.button("🏠", key="btn_dash", use_container_width=True):
            st.session_state.mobile_menu = "Dashboard"
            st.session_state.show_more = False
            st.rerun()

        if col2.button("👥", key="btn_memb", use_container_width=True):
            st.session_state.mobile_menu = "Members"
            st.session_state.show_more = False
            st.rerun()

        if col3.button("💰", key="btn_coll", use_container_width=True):
            st.session_state.mobile_menu = "Collections"
            st.session_state.show_more = False
            st.rerun()

        if col4.button("📊", key="btn_repo", use_container_width=True):
            st.session_state.mobile_menu = "Reports"
            st.session_state.show_more = False
            st.rerun()

        if col5.button("☰", key="btn_more", use_container_width=True):
            st.session_state.show_more = not st.session_state.get(
                "show_more", False
            )
            st.rerun()

    # Agar 'More' menu open hai, toh use bottom bar ke thoda upar dikhayenge
    if st.session_state.get("show_more", False):
        more_menu = st.selectbox(
            "More Options", ["Loans", "Donations", "Expenses"], index=0
        )
        st.session_state.mobile_menu = more_menu

    return st.session_state.get("mobile_menu", "Dashboard")

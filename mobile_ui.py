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
    # Direct HTML Component inject kar rahe hain jo pure layout container se azad hai
    st.markdown(
        """
        <div class="custom-bottom-nav">
            <button class="nav-btn" onclick="window.parent.location.search = '?nav=Dashboard'">🏠</button>
            <button class="nav-btn" onclick="window.parent.location.search = '?nav=Members'">👥</button>
            <button class="nav-btn" onclick="window.parent.location.search = '?nav=Collections'">💰</button>
            <button class="nav-btn" onclick="window.parent.location.search = '?nav=Reports'">📊</button>
            <button class="nav-btn" onclick="window.parent.location.search = '?nav=More'">☰</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # URL query arguments parse karke state maintain rakhna
    query_params = st.query_params
    if "nav" in query_params:
        selected_nav = query_params["nav"]
        if selected_nav == "More":
            st.session_state.show_more = True
        else:
            st.session_state.mobile_menu = selected_nav
            st.session_state.show_more = False

    # Agar More (☰) press kiya ho toh selective drop-down dikhana
    if st.session_state.get("show_more", False):
        more_menu = st.selectbox(
            "More Options",
            ["Loans", "Donations", "Expenses"],
            index=0
        )
        st.session_state.mobile_menu = more_menu

    return st.session_state.get("mobile_menu", "Dashboard")

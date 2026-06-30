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
                padding-bottom: 140px !important;
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

        /* Fixed Bottom Navigation */
        .mobile-bottom-nav{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            background: #111424;
            box-shadow: 0 -6px 20px rgba(0,0,0,0.5);
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
        <div style="
            color: #cbd5e1;
            font-size: 15px;
            margin-bottom: 12px;
        ">
            {title}
        </div>

        <div style="
            color: white;
            font-size: 26px;
            font-weight: 700;
        ">
            {value}
        </div>
    </div>
    """

    components.html(
        html_content,
        height=110,
        scrolling=False
    )

# ================= MOBILE NAVIGATION =================
def show_mobile_navigation():

    menu_options = [
        "Dashboard",
        "Members",
        "Collections",
        "Reports",
        "More"
    ]

    default_index = 0

    current_menu = st.session_state.get(
        "mobile_menu",
        "Dashboard"
    )

    if current_menu in menu_options:
        default_index = menu_options.index(current_menu)

    elif current_menu in [
        "Loans",
        "Donations",
        "Expenses"
    ]:
        default_index = 4

    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=[
            "house",
            "people",
            "wallet2",
            "bar-chart-line",
            "list"
        ],
        menu_icon="cast",
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#111424",
                "border-radius": "20px"
            },

            "icon": {
                "color": "#FFF",
                "font-size": "20px"
            },

            "nav-link": {
                "font-size": "0px",
                "text-align": "center",
                "margin": "0px",
                "padding": "14px 0px",
                "--hover-color": "rgba(255,255,255,0.1)"
            },

            "nav-link-selected": {
                "background-color": "#5856D6"
            },
        }
    )

    if selected == "More":
        st.session_state.mobile_menu = "Loans"
    else:
        st.session_state.mobile_menu = selected

    return st.session_state.mobile_menu

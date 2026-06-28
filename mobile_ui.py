import streamlit as st


# ================= DEVICE DETECTION =================
def is_mobile():

    user_agent = st.context.headers.get(
        "user-agent",
        ""
    ).lower()

    return (
        "android" in user_agent
        or
        "iphone" in user_agent
    )


# ================= MOBILE CSS =================
def load_mobile_css():

    st.markdown("""
    <style>

    @media (max-width:768px){

        .block-container{
            padding:12px !important;
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

    /* ================= MOBILE CARDS ================= */

    .mobile-balance-card{
        background: linear-gradient(
            135deg,
            rgba(139,92,246,0.85),
            rgba(79,70,229,0.85)
        );

        padding:22px;
        border-radius:22px;
        text-align:center;
        margin-bottom:18px;
        box-shadow:0 8px 24px rgba(0,0,0,0.35);
    }

    .mobile-balance-title{
        color:white;
        font-size:14px;
        opacity:0.9;
    }

    .mobile-balance-amount{
        color:white;
        font-size:34px;
        font-weight:700;
        margin-top:8px;
    }

    .mobile-card{
        background:rgba(255,255,255,0.05);
        backdrop-filter:blur(10px);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:18px;
        padding:18px;
        margin-bottom:12px;
        text-align:center;
    }

    .mobile-card-title{
        color:#cbd5e1;
        font-size:13px;
        margin-bottom:8px;
    }

    .mobile-card-value{
        color:white;
        font-size:24px;
        font-weight:700;
    }

    .section-title{
        color:#F8D568;
        font-size:18px;
        font-weight:600;
        margin-top:20px;
        margin-bottom:12px;
    }

    </style>
    """, unsafe_allow_html=True)


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

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(
                135deg,
                rgba(37,99,235,0.95),
                rgba(30,64,175,0.95)
            );

            border-radius:20px;
            padding:16px;
            margin-bottom:18px;
            box-shadow:0 8px 24px rgba(0,0,0,0.25);
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                ">

                    <img
                        src="logo.png"
                        width="50"
                        style="
                            border-radius:50%;
                        "
                    >

                    <div>

                        <div style="
                            color:white;
                            font-size:18px;
                            font-weight:700;
                        ">
                            बाल युवा मंगलदल समिति
                        </div>

                        <div style="
                            color:rgba(255,255,255,0.8);
                            font-size:13px;
                        ">
                            👋 Welcome, {username}
                        </div>

                    </div>

                </div>

                <div style="
                    font-size:24px;
                    color:white;
                ">
                    🔔
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ================= SECTION TITLE =================
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

    st.markdown(
        f"""
        <div class="mobile-card">

            <div class="mobile-card-title">
                {title}
            </div>

            <div class="mobile-card-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

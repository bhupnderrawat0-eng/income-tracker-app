# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Smart Finance Tracker",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

/* FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family: 'Poppins', sans-serif;
}

/* REMOVE TOP SPACE */
.block-container{
    padding-top: 1rem !important;
}

header[data-testid="stHeader"]{
    background: transparent;
}

/* HIDE STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* APP BACKGROUND */
.stApp{
    background:
    linear-gradient(rgba(8,15,35,0.82), rgba(8,15,35,0.82)),
    url("https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?q=80&w=1974&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: rgba(15,23,42,0.78);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] *{
    color: white !important;
}

/* LOGO CARD */
.logo-card{
    background: linear-gradient(
        135deg,
        rgba(30,41,59,0.82),
        rgba(15,23,42,0.82)
    );

    border-radius: 28px;
    padding: 30px;
    text-align: center;
    margin-bottom: 25px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

/* HERO CARD */
.hero-card{
    background: linear-gradient(
        135deg,
        rgba(30,41,59,0.82),
        rgba(15,23,42,0.82)
    );

    border-radius: 28px;
    padding: 35px;
    margin-bottom: 25px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

/* HERO TITLE */
.hero-title{
    font-size: 68px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

/* HERO SUB */
.hero-sub{
    font-size: 34px;
    font-weight: 700;
    color: white;
}

/* HERO TEXT */
.hero-text{
    font-size: 22px;
    color: #cbd5e1;
    margin-top: 8px;
}

/* METRIC CARD */
.metric-card{
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.35),
        rgba(96,165,250,0.25)
    );

    border-radius: 24px;
    padding: 28px;

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

/* METRIC TITLE */
.metric-title{
    font-size: 26px;
    font-weight: 700;
    color: white;
    margin-bottom: 12px;
}

/* METRIC VALUE */
.metric-value{
    font-size: 56px;
    font-weight: 800;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR LOGO
# =========================================
st.sidebar.markdown("""
<div class="logo-card">

    <div style="
        font-size:90px;
        margin-bottom:8px;
        filter:drop-shadow(0 0 12px rgba(255,120,0,0.55));
    ">
        🔥
    </div>

    <div style="
        font-size:34px;
        font-weight:800;
        color:white;
        line-height:1.1;
    ">
        Bal Yuva
    </div>

    <div style="
        font-size:34px;
        font-weight:800;
        color:#38bdf8;
        line-height:1.1;
    ">
        Mangal Dal
    </div>

    <div style="
        font-size:16px;
        letter-spacing:5px;
        color:#cbd5e1;
        margin-top:14px;
    ">
        SMART FINANCE TRACKER
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================
# MENU
# =========================================
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customers",
        "Collections",
        "Loans",
        "Donations",
        "Expenses",
        "Reports",
        "Users"
    ]
)

# =========================================
# DUMMY DATA
# =========================================
collections_total = 0
donations_total = 0
expenses_total = 0
customers_total = 0
balance = 0

# =========================================
# DASHBOARD
# =========================================
if menu == "Dashboard":

    st.markdown("""
    <div class="hero-card">

        <div class="hero-title">
            📊 Dashboard
        </div>

        <div class="hero-sub">
            Welcome back 👋
        </div>

        <div class="hero-text">
            Here's what's happening today.
        </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💵 Collections</div>
            <div class="metric-value">₹ {collections_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎁 Donations</div>
            <div class="metric-value">₹ {donations_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🛠️ Expenses</div>
            <div class="metric-value">₹ {expenses_total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">👥 Customers</div>
            <div class="metric-value">{customers_total}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📄 Net Balance</div>
        <div class="metric-value">₹ {balance}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# OTHER PAGES
# =========================================
else:
    st.title(menu)
    st.info(f"{menu} page coming soon...")

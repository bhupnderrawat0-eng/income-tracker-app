import streamlit as st
from streamlit_option_menu import option_menu

# Page Configurations - Dark Theme Setup
st.set_page_config(
    page_title="बाल युवा मंगलदल समिति",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Global Dark Theme Injection
st.markdown(
    """
    <style>
    /* Main Background Override */
    .stApp {
        background-color: #060814 !important;
        color: #FFFFFF !important;
    }
    
    /* Hide Default Streamlit Elements for App Feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container Padding Fix */
    .block-container {
        padding-top: 20px !important;
        padding-bottom: 50px !important;
        max-width: 500px !important; /* Perfect Mobile Width Frame */
    }
    
    /* Custom Styling for Streamlit Buttons inside Quick Actions */
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        color: #CBD5E1 !important;
        padding: 0 !important;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR NAVIGATION (Hamburger Menu) =================
with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; padding: 10px;'>
            <h3 style='color: #F8D568; margin-bottom: 20px;'>बाल युवा मंगलदल</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    selected_page = option_menu(
        menu_title=None,
        options=["Dashboard", "Members", "Collections", "Loans", "Expenses", "Reports"],
        icons=["house", "people", "wallet2", "cash-coin", "currency-exchange", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#0B0E1F", "padding": "5px"},
            "icon": {"color": "#FFF", "font-size": "18px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "5px", "color": "#CBD5E1"},
            "nav-link-selected": {"background-color": "#5856D6"},
        }
    )

# Render Content Based on Selection
if selected_page == "Dashboard":

    # ================= 1. PREMIUM HEADER =================
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px;">
            <div style="font-size: 24px; color: #cbd5e1; cursor: pointer;">☰</div>
            <div style="text-align: center; flex-grow: 1; margin-right: -24px;">
                <h3 style="color: #F8D568; font-size: 22px; margin: 0; font-weight: 700;">बाल युवा मंगलदल समिति</h3>
                <p style="color: #A0AEC0; font-size: 13px; margin: 2px 0 0 0;">👋 Welcome, admin</p>
            </div>
            <div style="font-size: 22px; color: #7F56D9; position: relative;">
                🔔<span style="position: absolute; top: -5px; right: -5px; background: #5856D6; color: white; font-size: 10px; padding: 1px 5px; border-radius: 50%;">3</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================= 2. HERO CARD (TOTAL BALANCE) =================
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #181336 0%, #0F0C24 100%); border: 1px solid #2A2456; border-radius: 20px; padding: 22px; position: relative; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="color: #94A3B8; font-size: 13px; letter-spacing: 0.5px;">Total Balance</div>
            <div style="color: #FFFFFF; font-size: 32px; font-weight: 700; margin-top: 5px;">₹ -23,500</div>
            <div style="color: #64748B; font-size: 11px; margin-top: 8px;">As on 29 Jun 2026</div>
            <div style="position: absolute; right: 25px; top: 50%; transform: translateY(-50%); font-size: 50px; opacity: 0.7;">👛</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================= 3. OVERVIEW GRID (2x2 Cards) =================
    st.markdown("<div style='color: #F8D568; font-size: 15px; font-weight: 600; margin-bottom: 12px;'>Overview</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="background: #11142A; border: 1px solid #1E2342; border-radius: 16px; padding: 16px; margin-bottom: 12px; display: flex; align-items: center;">
                <div style="background: rgba(88, 86, 214, 0.15); padding: 10px; border-radius: 12px; font-size: 20px; margin-right: 12px;">👥</div>
                <div>
                    <div style="color: #94A3B8; font-size: 11px;">Total Members</div>
                    <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-top: 2px;">125</div>
                    <div style="color: #475569; font-size: 10px; margin-top: 1px;">Active Members</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="background: #11142A; border: 1px solid #1E2342; border-radius: 16px; padding: 16px; margin-bottom: 12px; display: flex; align-items: center;">
                <div style="background: rgba(245, 158, 11, 0.15); padding: 10px; border-radius: 12px; font-size: 20px; margin-right: 12px;">💰</div>
                <div>
                    <div style="color: #94A3B8; font-size: 11px;">Total Loans</div>
                    <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-top: 2px;">₹ 2,10,000</div>
                    <div style="color: #475569; font-size: 10px; margin-top: 1px;">Total Disbursed</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="background: #11142A; border: 1px solid #1E2342; border-radius: 16px; padding: 16px; margin-bottom: 12px; display: flex; align-items: center;">
                <div style="background: rgba(16, 185, 129, 0.15); padding: 10px; border-radius: 12px; font-size: 20px; margin-right: 12px;">💵</div>
                <div>
                    <div style="color: #94A3B8; font-size: 11px;">Total Collections</div>
                    <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-top: 2px;">₹ 1,48,500</div>
                    <div style="color: #475569; font-size: 10px; margin-top: 1px;">This Month</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="background: #11142A; border: 1px solid #1E2342; border-radius: 16px; padding: 16px; margin-bottom: 12px; display: flex; align-items: center;">
                <div style="background: rgba(239, 68, 68, 0.15); padding: 10px; border-radius: 12px; font-size: 20px; margin-right: 12px;">📅</div>
                <div>
                    <div style="color: #94A3B8; font-size: 11px;">Pending Amount</div>
                    <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-top: 2px;">₹ 71,500</div>
                    <div style="color: #475569; font-size: 10px; margin-top: 1px;">Collections + Loans</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    # ================= 4. QUICK ACTIONS =================
    st.markdown("<div style='color: #F8D568; font-size: 15px; font-weight: 600; margin-top: 15px; margin-bottom: 12px;'>Quick Actions</div>", unsafe_allow_html=True)
    
    qa_cols = st.columns(5)
    actions = [
        {"icon": "➕", "label": "Add Member"},
        {"icon": "📥", "label": "Add Coll."},
        {"icon": "💸", "label": "Add Loan"},
        {"icon": "🧾", "label": "Add Exp."},
        {"icon": "📊", "label": "Reports"}
    ]
    
    for i, act in enumerate(actions):
        with qa_cols[i]:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <div style="background: #11142A; border: 1px solid #1E2342; width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                        {act['icon']}
                    </div>
                </div>
                """, unsafe_allow_html=True
            )
            # Clickable trigger buttons
            if st.button(act['label'], key=f"btn_{i}"):
                st.toast(f"Opening {act['label']}...")

    # ================= 5. RECENT ACTIVITY =================
    st.markdown(
        """
        <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 25px; margin-bottom: 12px;'>
            <span style='color: #F8D568; font-size: 15px; font-weight: 600;'>Recent Activity</span>
            <span style='color: #5856D6; font-size: 12px; cursor: pointer;'>View All ❯</span>
        </div>
        """, unsafe_allow_html=True
    )
    
    activities = [
        {"icon": "📥", "bg": "rgba(16, 185, 129, 0.12)", "title": "Collection Received", "sub": "MEM-1001 | Rajesh Kumar", "amt": "+ ₹2,000", "color": "#10B981", "date": "29 Jun 2026"},
        {"icon": "📤", "bg": "rgba(245, 158, 11, 0.12)", "title": "Loan Payment", "sub": "MEM-1003 | Suresh Patel", "amt": "+ ₹1,500", "color": "#10B981", "date": "28 Jun 2026"},
        {"icon": "🛒", "bg": "rgba(239, 68, 68, 0.12)", "title": "Expense Added", "sub": "Office Stationery", "amt": "- ₹850", "color": "#EF4444", "date": "28 Jun 2026"}
    ]
    
    for act in activities:
        st.markdown(
            f"""
            <div style="background: #11142A; border-bottom: 1px solid #1E2342; padding: 12px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <div style="background: {act['bg']}; width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px; font-size: 16px;">
                        {act['icon']}
                    </div>
                    <div>
                        <div style="color: #FFFFFF; font-size: 13px; font-weight: 600;">{act['title']}</div>
                        <div style="color: #64748B; font-size: 11px; margin-top: 1px;">{act['sub']}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="color: {act['color']}; font-size: 13px; font-weight: 700;">{act['amt']}</div>
                    <div style="color: #475569; font-size: 10px; margin-top: 1px;">{act['date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

else:
    # Sub-pages template placeholder
    st.markdown(f"<h2 style='color: #F8D568; text-align:center;'>{selected_page} Section</h2>", unsafe_allow_html=True)
    st.write(f"Yahan par aapka {selected_page} ka data load hoga.")

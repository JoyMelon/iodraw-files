import streamlit as st
import requests
import time

# 页面配置
st.set_page_config(
    page_title="奢华面试AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 奢华升级版
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@300;400;500;600&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --gold-light: #F5E6C8;
    --gold: #D4AF37;
    --gold-dark: #B8860B;
    --navy: #0A0E1C;
    --navy-light: #151930;
    --white-soft: rgba(255,255,255,0.7);
}

* {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.serif {
    font-family: 'Cormorant Garamond', serif;
}

.main {
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-light) 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 0 !important; padding-bottom: 0 !important;}

/* 奢华导航栏 */
.luxury-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: linear-gradient(180deg, rgba(10,14,28,0.95) 0%, rgba(10,14,28,0.85) 100%);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(212,175,55,0.15);
    padding: 1.5rem 2rem;
}

.nav-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    letter-spacing: 0.25em;
    color: var(--gold-light);
    text-transform: uppercase;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* 主内容区域 - 避开固定导航 */
.main-content {
    padding-top: 100px;
}

/* Hero区域 */
.hero {
    padding: 6rem 2rem 5rem;
    text-align: center;
    max-width: 1000px;
    margin: 0 auto;
}

.hero-logo {
    font-family: 'Playfair Display', serif;
    font-size: 0.9rem;
    letter-spacing: 0.4em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

.hero-title {
    font-size: 4.5rem;
    color: white;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    font-weight: 300;
}

.hero-highlight {
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dark) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
}

.hero-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.35rem;
    color: var(--white-soft);
    margin-bottom: 3rem;
    line-height: 1.6;
    font-weight: 300;
}

/* 区域通用样式 */
.section {
    padding: 5rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.section-label {
    text-align: center;
    font-size: 0.8rem;
    letter-spacing: 0.3em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    color: white;
    margin-bottom: 3rem;
    font-weight: 400;
}

/* 品牌展示网格 */
.brands-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    max-width: 1100px;
    margin: 0 auto;
    border-top: 1px solid rgba(212,175,55,0.15);
    border-left: 1px solid rgba(212,175,55,0.15);
}

.brand-cell {
    aspect-ratio: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-right: 1px solid rgba(212,175,55,0.15);
    border-bottom: 1px solid rgba(212,175,55,0.15);
    padding: 1.5rem;
    transition: all 0.4s ease;
    cursor: pointer;
    background: transparent;
}

.brand-cell:hover {
    background: rgba(212,175,55,0.06);
}

.brand-icon {
    font-size: 3rem;
    margin-bottom: 0.75rem;
    filter: drop-shadow(0 0 15px rgba(212,175,55,0.2));
}

.brand-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    color: var(--gold-light);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 500;
}

/* 功能网格 */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
    max-width: 1200px;
    margin: 0 auto;
}

.feature-item {
    padding: 3.5rem 2.5rem;
    border: 1px solid rgba(212,175,55,0.12);
    transition: all 0.4s ease;
}

.feature-item:nth-child(1),
.feature-item:nth-child(2),
.feature-item:nth-child(3) {
    border-top: none;
}

.feature-item:nth-child(1),
.feature-item:nth-child(4) {
    border-left: none;
}

.feature-item:nth-child(3),
.feature-item:nth-child(6) {
    border-right: none;
}

.feature-item:nth-child(4),
.feature-item:nth-child(5),
.feature-item:nth-child(6) {
    border-bottom: none;
}

.feature-item:hover {
    background: rgba(212,175,55,0.05);
}

.feature-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.8rem;
    color: var(--gold);
    letter-spacing: 0.2em;
    margin-bottom: 1.5rem;
}

.feature-icon {
    font-size: 2.25rem;
    margin-bottom: 1.25rem;
}

.feature-title {
    color: white;
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
    font-weight: 500;
}

.feature-desc {
    color: var(--white-soft);
    line-height: 1.7;
    font-size: 0.95rem;
    font-weight: 300;
}

/* CTA区域 */
.cta-section {
    padding: 6rem 2rem;
    text-align: center;
}

.cta-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.75rem;
    color: white;
    margin-bottom: 1rem;
    font-weight: 400;
}

.cta-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    color: var(--white-soft);
    margin-bottom: 2.5rem;
}

/* 页脚 */
.footer {
    border-top: 1px solid rgba(212,175,55,0.12);
    padding: 4rem 2rem 2rem;
    margin-top: 2rem;
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.footer-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    letter-spacing: 0.25em;
    color: var(--gold-light);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.footer-text {
    color: rgba(255,255,255,0.5);
    font-size: 0.9rem;
    max-width: 300px;
    line-height: 1.6;
}

.footer-links {
    display: flex;
    gap: 3rem;
}

.footer-column h4 {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1.25rem;
}

.footer-column a {
    display: block;
    color: rgba(255,255,255,0.5);
    text-decoration: none;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    transition: color 0.3s ease;
}

.footer-column a:hover {
    color: var(--gold-light);
}

.footer-bottom {
    max-width: 1200px;
    margin: 3rem auto 0;
    padding-top: 2rem;
    border-top: 1px solid rgba(212,175,55,0.1);
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.8rem;
    letter-spacing: 0.1em;
}

/* Streamlit按钮美化 */
.stButton > button {
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%) !important;
    color: var(--navy) !important;
    border: none !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-size: 0.85rem !important;
    padding: 0.85rem 2rem !important;
    border-radius: 2px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(212,175,55,0.3) !important;
}

.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--gold-light) !important;
    border: 1px solid rgba(212,175,55,0.4) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: rgba(212,175,55,0.08) !important;
    border-color: var(--gold) !important;
}

/* 模态框样式 */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(10,14,28,0.92);
    backdrop-filter: blur(15px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
}

.modal-box {
    background: linear-gradient(135deg, rgba(21,25,48,0.98) 0%, rgba(10,14,28,0.98) 100%);
    border: 1px solid rgba(212,175,55,0.25);
    padding: 3rem;
    max-width: 450px;
    width: 90%;
    position: relative;
}

.modal-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

.modal-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: white;
    margin-bottom: 0.5rem;
    text-align: center;
}

.modal-subtitle {
    color: var(--white-soft);
    text-align: center;
    margin-bottom: 2rem;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
}

/* Dashboard样式 */
.dashboard {
    padding: 3rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.dashboard-header {
    text-align: center;
    margin-bottom: 3rem;
}

.dashboard-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.25rem;
    color: white;
    margin-bottom: 0.5rem;
}

.dashboard-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    color: var(--white-soft);
}

/* Tab样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 2.5rem;
    border-bottom: 1px solid rgba(212,175,55,0.15);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--white-soft) !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 1rem 0 !important;
    font-family: 'Inter', sans-serif !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}
</style>
""", unsafe_allow_html=True)

# 初始化状态
API_BASE_URL = "http://localhost:8000"

if 'token' not in st.session_state:
    st.session_state.token = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = None

# 主页面渲染
def render_landing_page():
    # 奢华导航栏
    st.markdown('<div class="luxury-nav"><div class="nav-wrapper">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 4, 3])
    with col1:
        st.markdown('<div class="nav-brand">💎 LUXURY INTERVIEW AI</div>', unsafe_allow_html=True)
    with col3:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.session_state.token:
                if st.button("DASHBOARD", key="nav_dashboard", type="primary", use_container_width=True):
                    st.session_state.current_page = 'dashboard'
                    st.rerun()
            else:
                if st.button("SIGN IN", key="nav_login", type="secondary", use_container_width=True):
                    st.session_state.show_modal = 'login'
        with btn_col2:
            if st.session_state.token:
                if st.button("LOGOUT", key="nav_logout", use_container_width=True):
                    st.session_state.token = None
                    st.rerun()
            else:
                if st.button("JOIN", key="nav_join", type="primary", use_container_width=True):
                    st.session_state.show_modal = 'register'
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Hero区域
    st.markdown("""
    <div class="hero">
        <div class="hero-logo">✨ PREMIUM CAREER PLATFORM</div>
        <h1 class="hero-title">
            Master the Art of<br>
            <span class="hero-highlight">Luxury Interviews</span>
        </h1>
        <p class="hero-subtitle">
            Elevate your career in the world of luxury fashion, hospitality, and high-end brands.<br>
            Exclusive interview preparation designed for excellence.
        </p>
    """, unsafe_allow_html=True)
    
    # 主要按钮
    btn_col1, btn_col2, _ = st.columns([2, 2, 3])
    with btn_col1:
        if st.button("BEGIN YOUR JOURNEY", type="primary", key="hero_primary", use_container_width=True):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
                st.rerun()
    with btn_col2:
        if st.button("LEARN MORE", type="secondary", key="hero_secondary", use_container_width=True):
            pass
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 品牌展示
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">OUR PARTNERS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">The World\'s Finest Brands</h2>', unsafe_allow_html=True)
    st.markdown('<div class="brands-grid">', unsafe_allow_html=True)
    
    luxury_brands = [
        ("🏛️", "LOUIS VUITTON"),
        ("👜", "CHANEL"),
        ("👑", "HERMÈS"),
        ("💍", "CARTIER"),
        ("👠", "GUCCI"),
        ("⌚", "ROLEX"),
        ("👗", "DIOR"),
        ("💎", "BVLGARI"),
        ("🕶️", "PRADA"),
        ("🎩", "BURBERRY")
    ]
    
    for icon, name in luxury_brands:
        st.markdown(f"""
        <div class="brand-cell">
            <div class="brand-icon">{icon}</div>
            <div class="brand-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 核心功能
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">WHAT WE OFFER</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Premium Features</h2>', unsafe_allow_html=True)
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    features = [
        {
            "number": "01",
            "icon": "🎯",
            "title": "AI Interview Coach",
            "desc": "Intelligent question generation tailored for luxury brands, with real-time professional feedback."
        },
        {
            "number": "02",
            "icon": "📚",
            "title": "Brand Knowledge Base",
            "desc": "Complete archives of luxury brand history, culture, heritage, and exclusive insider information."
        },
        {
            "number": "03",
            "icon": "🎭",
            "title": "VIP Scenario Simulation",
            "desc": "Realistic high-end client service scenarios to elevate your professional service skills."
        },
        {
            "number": "04",
            "icon": "✨",
            "title": "Resume Polishing",
            "desc": "Transform ordinary resumes into luxury industry style, highlighting your distinctive advantages."
        },
        {
            "number": "05",
            "icon": "📊",
            "title": "Interview Analytics",
            "desc": "Comprehensive performance analysis with targeted improvement recommendations."
        },
        {
            "number": "06",
            "icon": "🌍",
            "title": "Multilingual Support",
            "desc": "Interview support in Chinese, English, French, and more for international brands."
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-item">
            <div class="feature-number">{feature["number"]}</div>
            <div class="feature-icon">{feature["icon"]}</div>
            <h3 class="feature-title">{feature["title"]}</h3>
            <p class="feature-desc">{feature["desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # CTA区域
    st.markdown('<div class="cta-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="cta-title">Ready to Begin?</h2>', unsafe_allow_html=True)
    st.markdown('<p class="cta-text">Join thousands of successful candidates who\'ve landed their dream jobs in the luxury industry</p>', unsafe_allow_html=True)
    
    cta_col1, cta_col2, cta_col3 = st.columns([2, 1, 2])
    with cta_col2:
        if st.button("GET STARTED", key="cta_final", type="primary", use_container_width=True):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 页脚
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div>
                <div class="footer-brand">💎 LUXURY INTERVIEW AI</div>
                <p class="footer-text">Your trusted partner for luxury career success. Premium interview preparation designed for excellence.</p>
            </div>
            <div class="footer-links">
                <div class="footer-column">
                    <h4>PRODUCT</h4>
                    <a href="#">AI Interview</a>
                    <a href="#">Brand Database</a>
                    <a href="#">Resume Tools</a>
                </div>
                <div class="footer-column">
                    <h4>COMPANY</h4>
                    <a href="#">About</a>
                    <a href="#">Contact</a>
                    <a href="#">Privacy</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            © 2024 LUXURY INTERVIEW AI. ALL RIGHTS RESERVED.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard_page():
    # 导航栏
    st.markdown('<div class="luxury-nav"><div class="nav-wrapper">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 4, 3])
    with col1:
        st.markdown('<div class="nav-brand">💎 LUXURY INTERVIEW AI</div>', unsafe_allow_html=True)
    with col3:
        if st.button("← HOME", key="db_home", type="secondary", use_container_width=True):
            st.session_state.current_page = 'landing'
            st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-content"><div class="dashboard">', unsafe_allow_html=True)
    
    # Dashboard头部
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">Welcome to Your Dashboard</h1>
        <p class="dashboard-subtitle">Your luxury career journey begins here</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Brand Knowledge", "💬 AI Interview", "📝 Resume Manager", "📊 Interview History"])
    
    with tab1:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 1.5rem;">Luxury Brand Knowledge Base</h3>', unsafe_allow_html=True)
        brands_info = [
            ("LOUIS VUITTON", "French luxury fashion house founded in 1854, renowned for its leather goods and monogram canvas"),
            ("CHANEL", "Parisian couture house established in 1910, famous for timeless elegance and the No.5 perfume"),
            ("HERMÈS", "French luxury goods manufacturer since 1837, specializing in leather, lifestyle accessories, and perfumes"),
            ("CARTIER", "The 'Jeweler of Kings', renowned for exquisite jewelry and watches since 1847"),
            ("GUCCI", "Italian luxury fashion brand founded in Florence in 1921, known for high-quality craftsmanship")
        ]
        
        for name, desc in brands_info:
            with st.expander(f"💎 {name}", expanded=False):
                st.write(desc)
                st.info("More brand knowledge coming soon...")
    
    with tab2:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 1.5rem;">Start Your AI Interview</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Select Target Brand", ["LOUIS VUITTON", "CHANEL", "HERMÈS", "GUCCI", "CARTIER"])
        with col2:
            st.selectbox("Interview Type", ["Brand Knowledge", "VIP Scenario", "Comprehensive"])
        
        if st.button("BEGIN INTERVIEW", type="primary"):
            st.info("Interview feature coming soon...")
    
    with tab3:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 1.5rem;">Resume Management</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF/DOCX)", type=['pdf', 'docx', 'doc'])
        if uploaded_file:
            st.success("Resume uploaded successfully!")
            if st.button("OPTIMIZE FOR LUXURY"):
                st.info("Resume optimization feature coming soon...")
    
    with tab4:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 1.5rem;">Interview History</h3>', unsafe_allow_html=True)
        st.info("No interviews yet. Start your first interview to see your history!")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def render_login_modal():
    if st.session_state.show_modal in ['login', 'register']:
        st.markdown('<div class="modal-overlay">', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="modal-box">', unsafe_allow_html=True)
            
            is_login = st.session_state.show_modal == 'login'
            
            st.markdown(f'<h2 class="modal-title">{"Sign In" if is_login else "Join Us"}</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="modal-subtitle">{"Welcome back. Please sign in to continue." if is_login else "Create your account and start your luxury career journey."}</p>', unsafe_allow_html=True)
            
            with st.form(key=f"luxury_{st.session_state.show_modal}"):
                if not is_login:
                    name = st.text_input("Full Name", placeholder="Your full name")
                    email = st.text_input("Email", placeholder="your@email.com")
                
                username = st.text_input("Username", placeholder="Choose a username")
                password = st.text_input("Password", type="password", placeholder="Your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("SIGN IN" if is_login else "CREATE ACCOUNT", type="primary", use_container_width=True)
                with col2:
                    cancel = st.form_submit_button("CANCEL", use_container_width=True)
                
                if cancel:
                    st.session_state.show_modal = None
                    st.rerun()
                
                if submit:
                    if is_login:
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/token",
                                data={"username": username, "password": password}
                            )
                            if response.status_code == 200:
                                token_data = response.json()
                                st.session_state.token = token_data["access_token"]
                                st.session_state.show_modal = None
                                st.session_state.current_page = 'dashboard'
                                st.success("Welcome back!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Invalid credentials. Please try again.")
                        except Exception as e:
                            st.error("Could not connect to server. Showing demo mode.")
                            st.session_state.token = "demo_token"
                            st.session_state.show_modal = None
                            st.session_state.current_page = 'dashboard'
                            st.rerun()
                    else:
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/register",
                                json={
                                    "username": username,
                                    "email": email if 'email' in locals() else "test@luxury.com",
                                    "full_name": name if 'name' in locals() else "User",
                                    "password": password
                                }
                            )
                            if response.status_code == 200:
                                st.success("Account created! Please sign in.")
                                st.session_state.show_modal = 'login'
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Registration failed. Please try again.")
                        except Exception as e:
                            st.error("Could not connect to server. Showing demo mode.")
                            st.session_state.token = "demo_token"
                            st.session_state.show_modal = None
                            st.session_state.current_page = 'dashboard'
                            st.rerun()
            
            st.markdown('</div></div>', unsafe_allow_html=True)

# 主渲染逻辑
if st.session_state.current_page == 'landing':
    render_landing_page()
elif st.session_state.current_page == 'dashboard':
    render_dashboard_page()

if st.session_state.show_modal:
    render_login_modal()

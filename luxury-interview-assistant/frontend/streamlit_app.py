import streamlit as st
import requests
import time

# 页面配置
st.set_page_config(
    page_title="LUXURY INTERVIEW AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 定制CSS - 极致奢华版
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --gold-light: #F5E6C8;
    --gold: #D4AF37;
    --gold-dark: #B8860B;
    --gold-deep: #8B6914;
    --navy: #0A0E1C;
    --navy-light: #151B30;
    --white: #FFFFFF;
    --white-soft: rgba(255,255,255,0.8);
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
    background: var(--navy);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 0 !important; padding-bottom: 0 !important;}

/* 奢华导航 */
.luxury-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: linear-gradient(180deg, rgba(10,14,28,0.95) 0%, rgba(10,14,28,0) 100%);
    padding: 2rem 4rem;
    backdrop-filter: blur(10px);
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
    font-size: 1.3rem;
    letter-spacing: 0.3em;
    color: var(--gold-light);
    text-transform: uppercase;
    font-weight: 600;
}

.nav-actions {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.nav-link {
    color: var(--white-soft);
    text-decoration: none;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: var(--gold);
}

/* Hero区域 - 全屏奢华 */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    inset: 0;
    background: 
        radial-gradient(circle at 20% 30%, rgba(212,175,55,0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(212,175,55,0.05) 0%, transparent 40%),
        linear-gradient(180deg, var(--navy) 0%, var(--navy-light) 100%);
}

.hero-pattern {
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23D4AF37' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.5;
}

.hero-content {
    position: relative;
    z-index: 10;
    text-align: center;
    max-width: 900px;
    padding: 0 2rem;
}

.hero-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    letter-spacing: 0.5em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 3rem;
    animation: fadeInDown 1s ease-out;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 5.5rem;
    font-weight: 300;
    color: var(--white);
    line-height: 1.1;
    margin-bottom: 2rem;
    animation: fadeInUp 1s ease-out 0.2s both;
}

.hero-title span {
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dark) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
}

.hero-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    color: var(--white-soft);
    font-weight: 300;
    letter-spacing: 0.05em;
    margin-bottom: 3.5rem;
    animation: fadeInUp 1s ease-out 0.4s both;
}

.hero-cta {
    animation: fadeInUp 1s ease-out 0.6s both;
}

/* 奢华按钮 */
.luxury-btn-primary {
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%);
    color: var(--navy);
    border: none;
    padding: 1.2rem 3.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.luxury-btn-primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.6s ease;
}

.luxury-btn-primary:hover::before {
    left: 100%;
}

.luxury-btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 60px rgba(212,175,55,0.3);
}

.luxury-btn-secondary {
    background: transparent;
    color: var(--gold-light);
    border: 1px solid rgba(212,175,55,0.4);
    padding: 1.15rem 3rem;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.4s ease;
}

.luxury-btn-secondary:hover {
    background: rgba(212,175,55,0.1);
    border-color: var(--gold);
}

/* 品牌展示区域 */
.brands-section {
    padding: 8rem 4rem;
    position: relative;
}

.brands-header {
    text-align: center;
    margin-bottom: 5rem;
}

.brands-label {
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.brands-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: var(--white);
    font-weight: 400;
}

.brands-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    max-width: 1200px;
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
    padding: 2rem;
    transition: all 0.5s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.brand-cell::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(212,175,55,0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.5s ease;
}

.brand-cell:hover {
    background: rgba(212,175,55,0.05);
}

.brand-cell:hover::before {
    opacity: 1;
}

.brand-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 20px rgba(212,175,55,0.2));
}

.brand-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: var(--gold-light);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 500;
}

/* 功能展示区域 */
.features-section {
    padding: 8rem 4rem;
    background: linear-gradient(180deg, transparent 0%, rgba(212,175,55,0.02) 100%);
}

.features-container {
    max-width: 1200px;
    margin: 0 auto;
}

.features-header {
    text-align: center;
    margin-bottom: 5rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
}

.feature-item {
    padding: 4rem 3rem;
    border: 1px solid rgba(212,175,55,0.1);
    transition: all 0.5s ease;
    position: relative;
}

.feature-item:nth-child(1) { border-top: none; border-left: none; }
.feature-item:nth-child(2) { border-top: none; }
.feature-item:nth-child(3) { border-top: none; border-right: none; }
.feature-item:nth-child(4) { border-left: none; border-bottom: none; }
.feature-item:nth-child(5) { border-bottom: none; }
.feature-item:nth-child(6) { border-right: none; border-bottom: none; }

.feature-item:hover {
    background: rgba(212,175,55,0.05);
}

.feature-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.8rem;
    color: var(--gold);
    letter-spacing: 0.2em;
    margin-bottom: 2rem;
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 2rem;
}

.feature-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--white);
    margin-bottom: 1rem;
    font-weight: 400;
}

.feature-text {
    color: var(--white-soft);
    line-height: 1.7;
    font-size: 0.95rem;
    font-weight: 300;
}

/* CTA区域 */
.cta-section {
    padding: 10rem 4rem;
    text-align: center;
    position: relative;
}

.cta-content {
    max-width: 700px;
    margin: 0 auto;
    position: relative;
    z-index: 10;
}

.cta-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: var(--white);
    margin-bottom: 1.5rem;
    font-weight: 400;
}

.cta-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    color: var(--white-soft);
    margin-bottom: 3rem;
    font-weight: 300;
}

/* 页脚 */
.footer {
    border-top: 1px solid rgba(212,175,55,0.1);
    padding: 5rem 4rem 3rem;
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
    font-size: 1.2rem;
    letter-spacing: 0.25em;
    color: var(--gold-light);
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.footer-text {
    color: rgba(255,255,255,0.5);
    font-size: 0.9rem;
    max-width: 300px;
    line-height: 1.7;
}

.footer-links {
    display: flex;
    gap: 4rem;
}

.footer-column h4 {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.footer-column a {
    display: block;
    color: rgba(255,255,255,0.5);
    text-decoration: none;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
    transition: color 0.3s ease;
}

.footer-column a:hover {
    color: var(--gold-light);
}

.footer-bottom {
    max-width: 1200px;
    margin: 4rem auto 0;
    padding-top: 2rem;
    border-top: 1px solid rgba(212,175,55,0.1);
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.8rem;
    letter-spacing: 0.1em;
}

/* 动画 */
@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Dashboard样式 */
.dashboard {
    min-height: 100vh;
    padding: 8rem 4rem 4rem;
}

.dashboard-wrapper {
    max-width: 1200px;
    margin: 0 auto;
}

.dashboard-header {
    text-align: center;
    margin-bottom: 4rem;
}

.dashboard-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: var(--white);
    margin-bottom: 1rem;
}

.dashboard-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    color: var(--white-soft);
}

/* 模态框 */
.modal {
    position: fixed;
    inset: 0;
    background: rgba(10,14,28,0.95);
    backdrop-filter: blur(20px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
}

.modal-box {
    background: linear-gradient(135deg, rgba(21,27,48,0.98) 0%, rgba(10,14,28,0.98) 100%);
    border: 1px solid rgba(212,175,55,0.2);
    padding: 4rem;
    max-width: 480px;
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
    font-size: 2rem;
    color: var(--white);
    margin-bottom: 0.5rem;
    text-align: center;
}

.modal-subtitle {
    color: var(--white-soft);
    text-align: center;
    margin-bottom: 2.5rem;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
}

.modal-input {
    width: 100%;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.15);
    padding: 1rem 1.25rem;
    color: var(--white);
    font-size: 0.95rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.modal-input:focus {
    outline: none;
    border-color: var(--gold);
    background: rgba(212,175,55,0.05);
}

/* Streamlit元素覆盖 */
.stButton > button {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    color: var(--white) !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    color: var(--white) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--white-soft);
    font-size: 0.9rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 1rem 0;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold);
    border-bottom: 1px solid var(--gold);
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

# 奢华品牌数据
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

# 功能数据
features_data = [
    {
        "number": "01",
        "icon": "🎯",
        "title": "AI Interview Coach",
        "text": "Intelligent question generation tailored for luxury brands, with real-time professional feedback."
    },
    {
        "number": "02",
        "icon": "📚",
        "title": "Brand Knowledge Base",
        "text": "Complete archives of luxury brand history, culture, heritage, and exclusive insider information."
    },
    {
        "number": "03",
        "icon": "🎭",
        "title": "VIP Scenario Simulation",
        "text": "Realistic high-end client service scenarios to elevate your professional service skills."
    },
    {
        "number": "04",
        "icon": "✨",
        "title": "Resume Polishing",
        "text": "Transform ordinary resumes into luxury industry style, highlighting your distinctive advantages."
    },
    {
        "number": "05",
        "icon": "📊",
        "title": "Interview Analytics",
        "text": "Comprehensive performance analysis with targeted improvement recommendations."
    },
    {
        "number": "06",
        "icon": "🌍",
        "title": "Multilingual Support",
        "text": "Interview support in Chinese, English, French, and more for international brands."
    }
]

# 渲染奢华首页
def render_luxury_landing():
    # 导航栏
    st.markdown('''
    <div class="luxury-nav">
        <div class="nav-wrapper">
            <div class="nav-brand">LUXURY INTERVIEW AI</div>
            <div class="nav-actions">
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3,1,1])
    with col2:
        if st.session_state.token:
            if st.button("DASHBOARD", key="nav_dashboard"):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        else:
            if st.button("SIGN IN", key="nav_login"):
                st.session_state.show_modal = 'login'
                st.rerun()
    with col3:
        if st.session_state.token:
            if st.button("LOGOUT", key="nav_logout"):
                st.session_state.token = None
                st.rerun()
        else:
            if st.button("JOIN", key="nav_join"):
                st.session_state.show_modal = 'register'
                st.rerun()
    
    st.markdown('''
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Hero区域
    st.markdown('''
    <div class="hero">
        <div class="hero-bg"></div>
        <div class="hero-pattern"></div>
        <div class="hero-content">
            <div class="hero-logo">💎 Premium Career Platform</div>
            <h1 class="hero-title">
                Master the Art of <span>Luxury</span> Interviews
            </h1>
            <p class="hero-subtitle">
                Elevate your career in the world of luxury fashion, hospitality, and high-end brands
            </p>
            <div class="hero-cta">
    ''', unsafe_allow_html=True)
    
    btn_col1, btn_col2, btn_col3 = st.columns([2,1,2])
    with btn_col2:
        if st.button("BEGIN YOUR JOURNEY", key="hero_cta", use_container_width=True):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
            st.rerun()
    
    st.markdown('''
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 品牌展示
    st.markdown('''
    <div class="brands-section">
        <div class="brands-header">
            <div class="brands-label">Our Partners</div>
            <h2 class="brands-title">The World's Finest Brands</h2>
        </div>
        <div class="brands-grid">
    ''', unsafe_allow_html=True)
    
    for icon, name in luxury_brands:
        st.markdown(f'''
        <div class="brand-cell">
            <div class="brand-icon">{icon}</div>
            <div class="brand-name">{name}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('''
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 功能展示
    st.markdown('''
    <div class="features-section">
        <div class="features-container">
            <div class="features-header">
                <div class="brands-label">What We Offer</div>
                <h2 class="brands-title">Premium Features</h2>
            </div>
            <div class="features-grid">
    ''', unsafe_allow_html=True)
    
    for feature in features_data:
        st.markdown(f'''
        <div class="feature-item">
            <div class="feature-number">{feature["number"]}</div>
            <div class="feature-icon">{feature["icon"]}</div>
            <h3 class="feature-title">{feature["title"]}</h3>
            <p class="feature-text">{feature["text"]}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('''
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # CTA区域
    st.markdown('''
    <div class="cta-section">
        <div class="cta-content">
            <h2 class="cta-title">Ready to Begin?</h2>
            <p class="cta-text">Join thousands of successful candidates who've landed their dream jobs in the luxury industry</p>
        </div>
    ''', unsafe_allow_html=True)
    
    cta_col1, cta_col2, cta_col3 = st.columns([2,1,2])
    with cta_col2:
        if st.button("GET STARTED", key="cta_final", use_container_width=True):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
            st.rerun()
    
    st.markdown('''
    </div>
    ''', unsafe_allow_html=True)
    
    # 页脚
    st.markdown('''
    <div class="footer">
        <div class="footer-content">
            <div>
                <div class="footer-brand">💎 LUXURY INTERVIEW AI</div>
                <p class="footer-text">Your trusted partner for luxury career success. Premium interview preparation designed for excellence.</p>
            </div>
            <div class="footer-links">
                <div class="footer-column">
                    <h4>Product</h4>
                    <a href="#">AI Interview</a>
                    <a href="#">Brand Database</a>
                    <a href="#">Resume Tools</a>
                </div>
                <div class="footer-column">
                    <h4>Company</h4>
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
    ''', unsafe_allow_html=True)

# Dashboard页面
def render_dashboard():
    # 导航栏
    st.markdown('''
    <div class="luxury-nav">
        <div class="nav-wrapper">
            <div class="nav-brand">LUXURY INTERVIEW AI</div>
            <div class="nav-actions">
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3,1,1])
    with col2:
        if st.button("← HOME", key="db_home"):
            st.session_state.current_page = 'landing'
            st.rerun()
    
    st.markdown('''
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Dashboard内容
    st.markdown('''
    <div class="dashboard">
        <div class="dashboard-wrapper">
            <div class="dashboard-header">
                <h1 class="dashboard-title">Welcome to Your Dashboard</h1>
                <p class="dashboard-subtitle">Your luxury career journey begins here</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Brand Knowledge", "💬 AI Interview", "📝 Resume Manager", "📊 Interview History"])
    
    with tab1:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 2rem;">Luxury Brand Knowledge Base</h3>', unsafe_allow_html=True)
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
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 2rem;">Start Your AI Interview</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Select Target Brand", ["LOUIS VUITTON", "CHANEL", "HERMÈS", "GUCCI", "CARTIER"])
        with col2:
            st.selectbox("Interview Type", ["Brand Knowledge", "VIP Scenario", "Comprehensive"])
        
        if st.button("BEGIN INTERVIEW"):
            st.info("Interview feature coming soon...")
    
    with tab3:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 2rem;">Resume Management</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF/DOCX)", type=['pdf', 'docx', 'doc'])
        if uploaded_file:
            st.success("Resume uploaded successfully!")
            if st.button("OPTIMIZE FOR LUXURY"):
                st.info("Resume optimization feature coming soon...")
    
    with tab4:
        st.markdown('<h3 style="color: white; font-family: Playfair Display, serif; margin-bottom: 2rem;">Interview History</h3>', unsafe_allow_html=True)
        st.info("No interviews yet. Start your first interview to see your history!")

# 模态框
def render_modal():
    if st.session_state.show_modal in ['login', 'register']:
        st.markdown('<div class="modal">', unsafe_allow_html=True)
        
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
                    submit = st.form_submit_button("SIGN IN" if is_login else "CREATE ACCOUNT", use_container_width=True)
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
                        except:
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
                        except:
                            st.error("Could not connect to server. Showing demo mode.")
                            st.session_state.token = "demo_token"
                            st.session_state.show_modal = None
                            st.session_state.current_page = 'dashboard'
                            st.rerun()
            
            st.markdown('</div></div>', unsafe_allow_html=True)

# 主渲染
if st.session_state.current_page == 'landing':
    render_luxury_landing()
elif st.session_state.current_page == 'dashboard':
    render_dashboard()

if st.session_state.show_modal:
    render_modal()

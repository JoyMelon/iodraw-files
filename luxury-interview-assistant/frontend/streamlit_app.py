import streamlit as st
import requests
from datetime import datetime
import time

# 页面配置
st.set_page_config(
    page_title="Luxury AI Interviewer",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400;500;600;700&family=Lato:wght@300;400;700&display=swap');
    
    :root {
        --primary-gold: #D4AF37;
        --dark-gold: #B8860B;
        --light-gold: #F4E4BA;
        --deep-navy: #0A0E27;
        --rich-purple: #2D1B69;
        --soft-black: #1A1A1A;
        --cream: #FDF8F0;
    }
    
    * {
        font-family: 'Lato', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        font-weight: 500;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #1A1A2E 50%, #0F0F23 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1128 0%, #151935 100%);
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Custom Container */
    .luxury-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(212,175,55,0.03) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(212,175,55,0.1);
    }
    
    /* Header Style */
    .page-header {
        background: linear-gradient(90deg, rgba(212,175,55,0.1) 0%, rgba(212,175,55,0.05) 100%);
        border-left: 4px solid var(--primary-gold);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--dark-gold) 100%);
        color: #0A0E27 !important;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-family: 'Lato', sans-serif;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(212,175,55,0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--dark-gold) 0%, var(--primary-gold) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212,175,55,0.4);
    }
    
    .secondary-btn > button {
        background: transparent;
        border: 1px solid var(--primary-gold);
        color: var(--primary-gold) !important;
        box-shadow: none;
    }
    
    .secondary-btn > button:hover {
        background: rgba(212,175,55,0.1);
        transform: none;
        box-shadow: 0 4px 15px rgba(212,175,55,0.2);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 8px;
        color: white;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-gold);
        box-shadow: 0 0 0 3px rgba(212,175,55,0.1);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(212,175,55,0.1) 0%, rgba(45,27,105,0.1) 100%);
        border: 1px solid rgba(212,175,55,0.25);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(212,175,55,0.2);
    }
    
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-gold) 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Divider */
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary-gold), transparent);
        margin: 2rem 0;
    }
    
    /* Success/Error Messages */
    .success-banner {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.05) 100%);
        border-left: 4px solid #4CAF50;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: #E8F5E9;
    }
    
    .error-banner {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.2) 0%, rgba(244, 67, 54, 0.05) 100%);
        border-left: 4px solid #F44336;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: #FFEBEE;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(212,175,55,0.05) !important;
        border: 1px solid rgba(212,175,55,0.2) !important;
        border-radius: 8px !important;
    }
    
    /* Logo/Brand */
    .brand-logo {
        text-align: center;
        padding: 2rem 0;
    }
    
    .brand-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, var(--primary-gold) 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 3px;
    }
    
    .brand-subtitle {
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* Welcome Page */
    .welcome-container {
        min-height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .hero-section {
        text-align: center;
        max-width: 800px;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #FFFFFF 0%, var(--primary-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.7);
        margin-bottom: 3rem;
        letter-spacing: 0.5px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(212,175,55,0.05);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255,255,255,0.7);
        border-radius: 8px;
        padding: 0.75rem 2rem;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--dark-gold) 100%);
        color: #0A0E27;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(212,175,55,0.05) 0%, rgba(45,27,105,0.05) 100%);
        border: 2px dashed rgba(212,175,55,0.3);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-gold);
        background: rgba(212,175,55,0.1);
    }
    
    /* Chat/Interview Container */
    .interview-container {
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        padding: 2rem;
    }
    
    .question-box {
        background: linear-gradient(135deg, rgba(45,27,105,0.2) 0%, rgba(212,175,55,0.1) 100%);
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    .shimmer {
        background: linear-gradient(90deg, rgba(212,175,55,0) 0%, rgba(212,175,55,0.2) 50%, rgba(212,175,55,0) 100%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }
    
    /* Icons */
    .icon-wrapper {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--dark-gold) 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 4px 15px rgba(212,175,55,0.3);
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .status-active {
        background: linear-gradient(135deg, rgba(76,175,80,0.2) 0%, rgba(76,175,80,0.05) 100%);
        color: #4CAF50;
        border: 1px solid rgba(76,175,80,0.3);
    }
    
    .status-completed {
        background: linear-gradient(135deg, rgba(33,150,243,0.2) 0%, rgba(33,150,243,0.05) 100%);
        color: #2196F3;
        border: 1px solid rgba(33,150,243,0.3);
    }
    
    /* Decorative Elements */
    .decorative-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.5), transparent);
        margin: 1.5rem 0;
    }
    
    .glow-effect {
        position: relative;
    }
    
    .glow-effect::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, var(--primary-gold), var(--dark-gold), var(--primary-gold));
        border-radius: inherit;
        z-index: -1;
        opacity: 0.5;
        filter: blur(10px);
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(45,27,105,0.03) 100%);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212,175,55,0.3);
        box-shadow: 0 12px 40px rgba(212,175,55,0.15);
    }
    
    .feature-icon {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, rgba(212,175,55,0.2) 0%, rgba(45,27,105,0.2) 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin: 0 auto 1rem;
        border: 1px solid rgba(212,175,55,0.2);
    }
    
    /* Loading Animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots span {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: var(--primary-gold);
        border-radius: 50%;
        margin: 0 2px;
        animation: pulse 1.4s ease-in-out infinite;
    }
    
    .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
    .loading-dots span:nth-child(3) { animation-delay: 0.4s; }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, var(--primary-gold) 0%, #FFD700 50%, var(--primary-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Floating Elements */
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .float {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Input Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500;
    }
    
    /* Form Submit Buttons */
    .stFormSubmitButton > button {
        width: 100% !important;
    }
    
    /* Background Pattern */
    .bg-pattern {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.03;
        background-image: 
            radial-gradient(circle at 25% 25%, var(--primary-gold) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, var(--primary-gold) 0%, transparent 50%);
        background-size: 100px 100px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# 应用常量
API_BASE_URL = "http://localhost:8000"

# 初始化session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'
if 'selected_resume_id' not in st.session_state:
    st.session_state.selected_resume_id = None
if 'current_interview_id' not in st.session_state:
    st.session_state.current_interview_id = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'interview_history' not in st.session_state:
    st.session_state.interview_history = []

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="brand-logo">
        <div class="brand-title">LUXE</div>
        <div class="brand-subtitle">AI INTERVIEWER</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.token:
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            user_response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
            if user_response.status_code == 200:
                user = user_response.json()
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 2rem;">
                    <div class="icon-wrapper" style="width: 72px; height: 72px; margin: 0 auto 1rem; font-size: 2rem;">
                        👤
                    </div>
                    <div style="color: white; font-weight: 600; font-size: 1.15rem; margin-bottom: 0.25rem;">{user.get('full_name', user['username'])}</div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">{user.get('email', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        except:
            pass
        
        st.markdown("<div class=\"decorative-line\"></div>", unsafe_allow_html=True)
        
        nav_options = [
            ("📋", "职位信息", "jobs"),
            ("📝", "简历管理", "resumes"), 
            ("🎯", "AI面试", "interview"),
            ("📊", "面试记录", "history")
        ]
        
        for icon, label, page_id in nav_options:
            button_style = "secondary" if st.session_state.current_page != page_id else "primary"
            if st.button(f"{icon} {label}", use_container_width=True, key=f"nav_{page_id}"):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.markdown("<div class=\"decorative-line\"></div>", unsafe_allow_html=True)
        
        if st.button("🚪 退出登录", use_container_width=True):
            st.session_state.token = None
            st.session_state.current_page = 'welcome'
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <div class="float" style="font-size: 4rem; margin-bottom: 1.5rem;">💎</div>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6;">
                欢迎使用奢侈品行业AI面试助手
            </p>
            <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 0.5rem;">
                请登录或注册以开始
            </p>
        </div>
        """, unsafe_allow_html=True)

# Welcome Page (Login/Register)
if st.session_state.current_page == 'welcome':
    st.markdown("""
    <div class="welcome-container fade-in">
        <div class="hero-section">
            <div class="float" style="font-size: 5rem; margin-bottom: 2rem;">💎✨</div>
            <h1 class="hero-title">LUXURY<br>INTERVIEWER</h1>
            <p class="hero-subtitle">为您量身定制的奢侈品行业AI面试助手<br>助力您进入梦想的奢华品牌</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, spacer, col2 = st.columns([1, 0.2, 1])
    
    with col1:
        st.markdown("""
        <div class="luxury-card fade-in glow-effect" style="animation-delay: 0.2s;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                <div class="icon-wrapper">🔐</div>
                <div>
                    <h3 style="margin: 0; color: white;">登录账户</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.9rem;">欢迎回来，请登录您的账户</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            login_username = st.text_input("用户名", placeholder="请输入用户名", key="login_user")
            login_password = st.text_input("密码", type="password", placeholder="请输入密码", key="login_pass")
            
            if st.form_submit_button("登录", use_container_width=True):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/token",
                        data={"username": login_username, "password": login_password}
                    )
                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state.token = token_data["access_token"]
                        st.session_state.current_page = 'jobs'
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-banner">登录失败，请检查用户名和密码</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-banner">登录失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="luxury-card fade-in glow-effect" style="animation-delay: 0.4s;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                <div class="icon-wrapper">✨</div>
                <div>
                    <h3 style="margin: 0; color: white;">注册新用户</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.9rem;">创建账户，开始您的奢侈品之旅</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=False):
            reg_username = st.text_input("用户名", placeholder="请设置用户名", key="reg_user")
            reg_email = st.text_input("邮箱", placeholder="请输入邮箱地址", key="reg_email")
            reg_fullname = st.text_input("姓名", placeholder="请输入您的姓名", key="reg_name")
            reg_password = st.text_input("密码", type="password", placeholder="请设置密码", key="reg_pass")
            
            if st.form_submit_button("注册", use_container_width=True):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/register",
                        json={
                            "username": reg_username,
                            "email": reg_email,
                            "full_name": reg_fullname,
                            "password": reg_password
                        }
                    )
                    if response.status_code == 200:
                        st.markdown(f'<div class="success-banner">🎉 注册成功！请登录</div>', unsafe_allow_html=True)
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-banner">注册失败: {response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-banner">注册失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("<div class=\"gold-divider\"></div>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align: center; color: white; margin-bottom: 2rem;\">🌟 核心功能</h3>", unsafe_allow_html=True)
    
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("📚", "品牌知识库", "深度了解奢侈品牌文化"),
        ("🎭", "VIP场景模拟", "真实模拟高端客户服务"),
        ("🎯", "AI智能评估", "多维度分析您的表现"),
        ("✨", "简历优化", "专为奢侈品行业打造")
    ]
    
    for idx, (icon, title, desc) in enumerate(features):
        with [f1, f2, f3, f4][idx]:
            st.markdown(f"""
            <div class="feature-card fade-in" style="animation-delay: {0.5 + idx * 0.1}s;">
                <div class="feature-icon">{icon}</div>
                <h4 style="color: var(--primary-gold); margin: 0 0 0.5rem;">{title}</h4>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# Jobs Page
elif st.session_state.current_page == 'jobs':
    st.markdown("""
    <div class="page-header fade-in">
        <h2 style="margin: 0; color: white;">📋 职位信息</h2>
        <p style="margin: 0.5rem 0 0; color: rgba(255,255,255,0.6);">浏览和发布奢侈品行业职位</p>
    </div>
    """, unsafe_allow_html=True)
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="luxury-card fade-in" style="animation-delay: 0.1s;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div class="icon-wrapper">➕</div>
                <div>
                    <h3 style="margin: 0; color: white;">发布新职位</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">添加新的奢侈品行业职位</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("post_job_form"):
            job_title = st.text_input("职位名称", placeholder="例如：精品店销售顾问")
            job_company = st.text_input("公司名称", placeholder="例如：Louis Vuitton")
            job_brand = st.selectbox("目标品牌", ["Louis Vuitton", "Chanel", "Hermès", "Gucci", "Cartier", "Dior", "Prada", "其他"])
            job_location = st.text_input("工作地点", placeholder="例如：上海")
            job_description = st.text_area("职位描述", placeholder="请描述职位职责...", height=100)
            job_requirements = st.text_area("任职要求", placeholder="请描述任职要求...", height=100)
            
            if st.form_submit_button("发布职位"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/jobs/post",
                        json={
                            "title": job_title,
                            "company": job_company,
                            "description": job_description,
                            "requirements": job_requirements,
                            "brand": job_brand,
                            "location": job_location
                        },
                        headers=headers
                    )
                    if response.status_code == 200:
                        st.markdown(f'<div class="success-banner">🎉 职位发布成功！</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-banner">发布失败: {response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-banner">发布失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="luxury-card fade-in" style="animation-delay: 0.2s;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div class="icon-wrapper">🏢</div>
                <div>
                    <h3 style="margin: 0; color: white;">职位列表</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">浏览可用的职位信息</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            jobs_response = requests.get(f"{API_BASE_URL}/jobs/legacy", headers=headers)
            if jobs_response.status_code == 200:
                jobs = jobs_response.json()
                if jobs:
                    for idx, job in enumerate(jobs):
                        with st.expander(f"{job['company']} - {job['position']}", expanded=False):
                            st.markdown(f"""
                            <div style="padding: 1rem;">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;">
                                    <div>
                                        <h4 style="color: var(--primary-gold); margin: 0 0 0.5rem; font-size: 1.2rem;">{job['position']}</h4>
                                        <div style="color: white; font-weight: 600; font-size: 1.1rem;">{job['company']}</div>
                                    </div>
                                    <span class="status-badge status-active">招聘中</span>
                                </div>
                                <div style="color: rgba(255,255,255,0.7); margin-bottom: 1rem; line-height: 1.7;">
                                    <strong style="color: var(--primary-gold);">📋 要求：</strong><br>{job['requirement']}
                                </div>
                                {f'<div style="color: rgba(255,255,255,0.6); line-height: 1.6;"><strong style="color: var(--primary-gold);">📝 描述：</strong><br>{job["description"]}</div>' if job.get('description') else ''}
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("暂无职位信息")
        except Exception as e:
            st.markdown(f'<div class="error-banner">获取职位失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Resumes Page
elif st.session_state.current_page == 'resumes':
    st.markdown("""
    <div class="page-header fade-in">
        <h2 style="margin: 0; color: white;">📝 简历管理</h2>
        <p style="margin: 0.5rem 0 0; color: rgba(255,255,255,0.6);">上传、管理和优化您的简历</p>
    </div>
    """, unsafe_allow_html=True)
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="luxury-card fade-in" style="animation-delay: 0.1s;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div class="icon-wrapper">📄</div>
                <div>
                    <h3 style="margin: 0; color: white;">上传简历文件</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">支持PDF、Word、TXT格式</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("选择简历文件", type=['pdf', 'docx', 'doc', 'txt'], label_visibility="collapsed")
        
        if uploaded_file and st.button("上传并解析", key="upload_file_btn", use_container_width=True):
            with st.spinner("正在解析简历..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(
                        f"{API_BASE_URL}/upload/resume",
                        files=files,
                        headers=headers
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.selected_resume_id = result['resume_id']
                        st.markdown(f'<div class="success-banner">🎉 简历上传成功！</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-banner">上传失败: {response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-banner">上传失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="gold-divider"></div>
            <div style="text-align: center; color: rgba(255,255,255,0.4); margin-bottom: 1.5rem;">
                <span style="font-size: 1.5rem;">✦</span><br>
                或
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div class="icon-wrapper">✏️</div>
                <div>
                    <h3 style="margin: 0; color: white; font-size: 1.1rem;">粘贴简历内容</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">直接输入您的简历内容</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("paste_resume_form"):
            resume_name = st.text_input("简历名称", placeholder="您的姓名")
            resume_text = st.text_area("简历内容", placeholder="请在此粘贴您的简历内容...", height=200)
            
            if st.form_submit_button("提交简历"):
                if resume_name and resume_text:
                    with st.spinner("正在处理简历..."):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/upload/resume/text",
                                data={"name": resume_name, "resume_text": resume_text},
                                headers=headers
                            )
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state.selected_resume_id = result['resume_id']
                                st.markdown(f'<div class="success-banner">🎉 简历提交成功！</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="error-banner">提交失败: {response.text}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f'<div class="error-banner">提交失败: {str(e)}</div>', unsafe_allow_html=True)
                else:
                    st.warning("请填写简历名称和内容")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="luxury-card fade-in" style="animation-delay: 0.2s;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div class="icon-wrapper">📂</div>
                <div>
                    <h3 style="margin: 0; color: white;">我的简历</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">查看和管理您的简历</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            resumes_response = requests.get(f"{API_BASE_URL}/resumes", headers=headers)
            if resumes_response.status_code == 200:
                resumes = resumes_response.json()
                if resumes:
                    for resume in resumes:
                        with st.expander(f"📄 {resume['name']} - 评分: {resume['score']:.1f}/10", expanded=False):
                            st.markdown(f"""
                            <div style="padding: 0.5rem;">
                                <div style="margin-bottom: 1.5rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                        <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">
                                            📅 上传时间: {resume.get('created_at', 'N/A')}
                                        </div>
                                        <span class="status-badge status-completed">已处理</span>
                                    </div>
                                    {f'<div style="color: rgba(255,255,255,0.5); font-size: 0.85rem; margin-bottom: 0.5rem;">📁 {resume.get("original_filename", "")}</div>' if resume.get('original_filename') else ''}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"选择此简历", key=f"select_{resume['id']}", use_container_width=True):
                                st.session_state.selected_resume_id = resume['id']
                                st.markdown(f'<div class="success-banner">✅ 简历已选择！</div>', unsafe_allow_html=True)
                            
                            if resume.get('optimization_suggestions') or resume.get('luxury_translated_version'):
                                st.markdown("<div class=\"decorative-line\"></div>", unsafe_allow_html=True)
                            
                            if resume.get('optimization_suggestions'):
                                st.markdown("""
                                <h4 style="color: var(--primary-gold); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                                    <span>💡</span> 优化建议
                                </h4>
                                """, unsafe_allow_html=True)
                                st.info(resume['optimization_suggestions'])
                            
                            if resume.get('luxury_translated_version'):
                                st.markdown("""
                                <h4 style="color: var(--primary-gold); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                                    <span>✨</span> 奢侈品行业版本
                                </h4>
                                """, unsafe_allow_html=True)
                                st.info(resume['luxury_translated_version'])
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 3rem 1rem; color: rgba(255,255,255,0.5);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                        <p>您还没有上传简历</p>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="error-banner">获取简历失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Interview Page
elif st.session_state.current_page == 'interview':
    st.markdown("""
    <div class="page-header fade-in">
        <h2 style="margin: 0; color: white;">🎯 AI面试</h2>
        <p style="margin: 0.5rem 0 0; color: rgba(255,255,255,0.6);">开始您的奢侈品行业模拟面试</p>
    </div>
    """, unsafe_allow_html=True)
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    if not st.session_state.current_interview_id:
        st.markdown("""
        <div class="luxury-card fade-in">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                <div class="icon-wrapper">🚀</div>
                <div>
                    <h3 style="margin: 0; color: white;">准备面试</h3>
                    <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.9rem;">选择简历和职位，开始您的模拟面试</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            try:
                resumes_response = requests.get(f"{API_BASE_URL}/resumes", headers=headers)
                resumes = resumes_response.json() if resumes_response.status_code == 200 else []
                
                if resumes:
                    resume_options = {f"{r['name']} (评分: {r['score']:.1f}/10)": r['id'] for r in resumes}
                    selected_resume_label = st.selectbox("选择简历", list(resume_options.keys()))
                    selected_resume_id = resume_options[selected_resume_label]
                else:
                    st.warning("请先上传简历")
                    st.stop()
            except Exception as e:
                st.markdown(f'<div class="error-banner">获取简历失败: {str(e)}</div>', unsafe_allow_html=True)
                st.stop()
        
        with col2:
            try:
                jobs_response = requests.get(f"{API_BASE_URL}/jobs/legacy", headers=headers)
                jobs = jobs_response.json() if jobs_response.status_code == 200 else []
                
                if jobs:
                    job_options = {f"{j['company']} - {j['position']}": j['id'] for j in jobs}
                    selected_job_label = st.selectbox("选择面试职位", list(job_options.keys()))
                    selected_job_id = job_options[selected_job_label]
                else:
                    st.warning("暂无可用职位")
                    st.stop()
            except Exception as e:
                st.markdown(f'<div class="error-banner">获取职位失败: {str(e)}</div>', unsafe_allow_html=True)
                st.stop()
        
        if st.button("开始面试", type="primary", use_container_width=True):
            with st.spinner("准备面试..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/interview/start",
                        params={"resume_id": selected_resume_id, "job_id": selected_job_id},
                        headers=headers
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.current_interview_id = result['interview_id']
                        st.session_state.current_question = result['question']
                        st.session_state.interview_history = []
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-banner">开始面试失败: {response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-banner">开始面试失败: {str(e)}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="interview-container fade-in">
        """, unsafe_allow_html=True)
        
        if st.session_state.current_question:
            st.markdown("""
            <div class="question-box">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                    <div class="icon-wrapper" style="width: 44px; height: 44px; font-size: 1.35rem;">🤔</div>
                    <div>
                        <h3 style="margin: 0; color: var(--primary-gold);">面试官问题</h3>
                        <p style="margin: 0.25rem 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">请认真思考并回答</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <p style="color: white; font-size: 1.35rem; line-height: 1.8; margin: 0;">
                    {st.session_state.current_question}
                </p>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div style=\"height: 2rem;\"></div>", unsafe_allow_html=True)
            
            answer = st.text_area("您的回答", placeholder="请在此输入您的回答...", height=180)
            
            if st.button("提交回答", type="primary", use_container_width=True):
                with st.spinner("AI正在分析您的回答..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/interview/answer",
                            params={
                                "interview_id": st.session_state.current_interview_id,
                                "answer": answer
                            },
                            headers=headers
                        )
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.session_state.interview_history.append({
                                "question": st.session_state.current_question,
                                "answer": answer,
                                "analysis": result['analysis']
                            })
                            
                            st.markdown("<div class=\"decorative-line\"></div>", unsafe_allow_html=True)
                            
                            st.subheader("📊 AI分析结果")
                            
                            analysis = result['analysis']
                            m1, m2, m3 = st.columns(3)
                            
                            with m1:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 0.75rem;">🏷️ 品牌匹配度</div>
                                    <div class="metric-value">{analysis['brand_match_score']:.1f}</div>
                                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">/10</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with m2:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 0.75rem;">💬 语气优雅度</div>
                                    <div class="metric-value">{analysis['tone_score']:.1f}</div>
                                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">/10</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with m3:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 0.75rem;">😊 情绪评分</div>
                                    <div class="metric-value">{analysis['emotion_score']:.1f}</div>
                                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">/10</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            <div class="luxury-card" style="margin-top: 2rem;">
                                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem;">
                                    <div class="icon-wrapper" style="width: 40px; height: 40px; font-size: 1.15rem;">💬</div>
                                    <h4 style="margin: 0; color: white;">详细反馈</h4>
                                </div>
                            """, unsafe_allow_html=True)
                            st.write(analysis['ai_analysis'])
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            if result['interview_complete']:
                                st.markdown("<div class=\"decorative-line\"></div>", unsafe_allow_html=True)
                                st.success(f"🎉 面试完成！总分: {result['total_score']:.1f}/10")
                                st.session_state.current_interview_id = None
                                st.session_state.current_question = None
                                if st.button("再试一次", use_container_width=True):
                                    st.rerun()
                            else:
                                st.session_state.current_question = result['next_question']
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.markdown(f'<div class="error-banner">提交失败: {response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-banner">提交失败: {str(e)}</div>', unsafe_allow_html=True)
        
        if st.session_state.interview_history:
            st.markdown("<div class=\"decorative-line\"></div>", unsafe_allow_html=True)
            st.subheader("📝 面试历史")
            for i, item in enumerate(reversed(st.session_state.interview_history)):
                with st.expander(f"问题 {len(st.session_state.interview_history) - i}", expanded=False):
                    st.markdown(f"""
                    <div style="margin-bottom: 1.25rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(212,175,55,0.1);">
                        <div style="color: var(--primary-gold); font-weight: 600; font-size: 1.05rem; margin-bottom: 0.75rem;">问:</div>
                        <div style="color: rgba(255,255,255,0.9); line-height: 1.7;">{item['question']}</div>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <div style="color: #4CAF50; font-weight: 600; font-size: 1.05rem; margin-bottom: 0.75rem;">答:</div>
                        <div style="color: rgba(255,255,255,0.8); line-height: 1.7;">{item['answer']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# History Page
elif st.session_state.current_page == 'history':
    st.markdown("""
    <div class="page-header fade-in">
        <h2 style="margin: 0; color: white;">📊 面试记录</h2>
        <p style="margin: 0.5rem 0 0; color: rgba(255,255,255,0.6);">查看您的历史面试记录和分析</p>
    </div>
    """, unsafe_allow_html=True)
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    try:
        interviews_response = requests.get(f"{API_BASE_URL}/interviews", headers=headers)
        if interviews_response.status_code == 200:
            interviews = interviews_response.json()
            if interviews:
                for interview in interviews:
                    status_display = {
                        "waiting": ("🟡", "等待中", "status-active"),
                        "answering": ("🟢", "进行中", "status-active"),
                        "resolved": ("🔵", "已完成", "status-completed")
                    }.get(interview.get('status', 'waiting'), ("⚪", "未知", ""))
                    
                    with st.expander(f"{status_display[0]} 面试 #{interview['id']} - 评分: {interview['score']:.1f}/10", expanded=False):
                        st.markdown(f"""
                        <div style="padding: 0.5rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                                <div>
                                    <div style="color: white; font-weight: 600; font-size: 1.2rem;">面试 #{interview['id']}</div>
                                    <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                                        📅 {interview.get('created_at', 'N/A')}
                                    </div>
                                </div>
                                <span class="status-badge {status_display[2]}">{status_display[1]}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        try:
                            detail_response = requests.get(
                                f"{API_BASE_URL}/interview/{interview['id']}",
                                headers=headers
                            )
                            if detail_response.status_code == 200:
                                detail = detail_response.json()
                                if 'rounds' in detail and detail['rounds']:
                                    st.markdown("""
                                    <div class="gold-divider"></div>
                                    <h4 style="color: var(--primary-gold); margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.75rem;">
                                        <span style="font-size: 1.35rem;">💬</span> 面试问题
                                    </h4>
                                    """, unsafe_allow_html=True)
                                    
                                    for r_idx, round_item in enumerate(detail['rounds']):
                                        st.markdown(f"""
                                        <div style="background: rgba(212,175,55,0.05); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem; border-left: 3px solid var(--primary-gold);">
                                            <div style="color: var(--primary-gold); font-weight: 600; font-size: 1.05rem; margin-bottom: 0.75rem;">
                                                问题 {r_idx + 1}
                                            </div>
                                            <div style="color: white; line-height: 1.7; margin-bottom: 1rem;">
                                                {round_item['question']}
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                                        if round_item.get('user_answer'):
                                            st.markdown(f"""
                                            <div style="margin-left: 1.5rem; padding-left: 1.25rem; border-left: 2px solid rgba(212,175,55,0.2);">
                                                <div style="color: #4CAF50; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem;">您的回答:</div>
                                                <div style="color: rgba(255,255,255,0.85); line-height: 1.7; margin-bottom: 0.75rem;">
                                                    {round_item['user_answer']}
                                                </div>
                                                <div style="display: flex; gap: 1.5rem; margin-bottom: 0.75rem; flex-wrap: wrap;">
                                                    <span style="color: rgba(212,175,55,0.9); font-size: 0.9rem; font-weight: 500;">🏷️ 品牌匹配: {round_item['brand_match_score']:.1f}/10</span>
                                                    <span style="color: rgba(212,175,55,0.9); font-size: 0.9rem; font-weight: 500;">💬 语气: {round_item['tone_score']:.1f}/10</span>
                                                </div>
                                                {f'<div style="color: rgba(255,255,255,0.65); line-height: 1.7; font-size: 0.95rem;">{round_item.get("ai_analysis", "")}</div>' if round_item.get('ai_analysis') else ''}
                                            </div>
                                            """, unsafe_allow_html=True)
                                        
                                        st.markdown("</div>", unsafe_allow_html=True)
                        except Exception as e:
                            pass
            else:
                st.markdown("""
                <div class="luxury-card" style="text-align: center; padding: 5rem 2rem;">
                    <div class="float" style="font-size: 5rem; margin-bottom: 1.5rem;">📭</div>
                    <h3 style="color: white; margin-bottom: 0.75rem;">暂无面试记录</h3>
                    <p style="color: rgba(255,255,255,0.6); font-size: 1rem; margin-bottom: 2rem;">开始您的第一次AI面试吧！</p>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-banner">获取面试记录失败: {str(e)}</div>', unsafe_allow_html=True)

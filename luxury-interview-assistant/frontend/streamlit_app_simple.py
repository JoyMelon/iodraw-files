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

# 自定义CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --gold-primary: #D4AF37;
    --gold-dark: #B8860B;
    --navy-dark: #0A0E27;
    --navy-medium: #151935;
}

* {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif;
}

.main {
    background: linear-gradient(180deg, #0A0E27 0%, #0F1328 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* 导航栏 */
.navbar {
    background: rgba(10, 14, 39, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(212, 175, 55, 0.1);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: white;
    font-size: 1.25rem;
    font-weight: 700;
}

/* 英雄区域 */
.hero {
    padding: 5rem 2rem;
    text-align: center;
    max-width: 1000px;
    margin: 0 auto;
}

.hero-title {
    font-size: 4rem;
    color: white;
    line-height: 1.1;
    margin-bottom: 1.5rem;
}

.hero-highlight {
    background: linear-gradient(135deg, var(--gold-primary) 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 2.5rem;
    line-height: 1.6;
}

/* 区域标题 */
.section {
    padding: 4rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.section-title {
    text-align: center;
    font-size: 2rem;
    color: white;
    margin-bottom: 2.5rem;
}

/* 功能卡片 */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.feature-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(212,175,55,0.03) 100%);
    border: 1px solid rgba(212,175,55,0.1);
    border-radius: 16px;
    padding: 2rem;
    transition: all 0.3s;
}

.feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(212,175,55,0.3);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.feature-title {
    color: var(--gold-primary);
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
}

.feature-desc {
    color: rgba(255,255,255,0.7);
    line-height: 1.6;
}

/* 平台网格 */
.platforms-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1.5rem;
    max-width: 1000px;
    margin: 0 auto;
}

.platform-item {
    background: rgba(212,175,55,0.05);
    border: 1px solid rgba(212,175,55,0.1);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s;
}

.platform-item:hover {
    border-color: rgba(212,175,55,0.3);
    transform: translateY(-4px);
}

.platform-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.platform-name {
    color: white;
    font-size: 0.875rem;
    font-weight: 500;
}

/* 页脚 */
.footer {
    border-top: 1px solid rgba(212,175,55,0.1);
    padding: 3rem 2rem 2rem;
    margin-top: 3rem;
    text-align: center;
}

.footer-text {
    color: rgba(255,255,255,0.5);
}

/* 动画 */
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.float {
    animation: float 3s ease-in-out infinite;
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
    # 导航栏
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.markdown('<div class="logo"><span style="font-size:1.75rem">💎</span><span>奢华面试AI</span></div>', unsafe_allow_html=True)
    with col3:
        if st.session_state.token:
            if st.button("进入系统", type="primary", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
            if st.button("退出", use_container_width=True):
                st.session_state.token = None
                st.rerun()
        else:
            if st.button("立即登录", type="primary", use_container_width=True):
                st.session_state.show_modal = 'login'

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # 英雄区域
    st.markdown("""
    <div class="hero fade-in">
        <div class="float" style="font-size: 4rem; margin-bottom: 1.5rem">💎✨</div>
        <h1 class="hero-title">
            奢华面试AI<br>
            <span class="hero-highlight">助你轻松拿OFFER</span>
        </h1>
        <p class="hero-subtitle">
            专为奢侈品行业打造的AI面试助手<br>
            深度品牌知识 · VIP场景模拟 · 专业面试训练
        </p>
    """, unsafe_allow_html=True)

    # 主要按钮
    btn_col1, btn_col2, _ = st.columns([2, 2, 3])
    with btn_col1:
        if st.button("免费使用", type="primary", use_container_width=True):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
                st.rerun()
    with btn_col2:
        if st.button("了解更多", use_container_width=True):
            pass
    st.markdown("</div>", unsafe_allow_html=True)

    # 平台支持
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">支持所有顶级奢侈品牌</h2>', unsafe_allow_html=True)
    st.markdown('<div class="platforms-grid">', unsafe_allow_html=True)
    
    platforms = [
        ("🏛️", "路易威登"),
        ("👜", "香奈儿"),
        ("👑", "爱马仕"),
        ("💍", "卡地亚"),
        ("👠", "古驰"),
        ("⌚", "劳力士"),
        ("👗", "迪奥"),
        ("💎", "宝格丽")
    ]
    
    for icon, name in platforms:
        st.markdown(f"""
        <div class="platform-item">
            <div class="platform-icon">{icon}</div>
            <div class="platform-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # 核心功能
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">奢华面试AI核心功能</h2>', unsafe_allow_html=True)
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    features = [
        {
            "icon": "🎯",
            "title": "AI面试助手",
            "desc": "智能生成奢侈品行业面试问题，提供专业回答建议与实时反馈"
        },
        {
            "icon": "📚",
            "title": "品牌知识库",
            "desc": "完整收录各大奢侈品牌历史、文化、经典产品与最新动态"
        },
        {
            "icon": "🎭",
            "title": "VIP场景模拟",
            "desc": "真实模拟高端客户服务场景，提升您的专业应对能力"
        },
        {
            "icon": "✨",
            "title": "AI简历优化",
            "desc": "将普通简历转化为奢侈品行业风格，突出您的核心优势"
        },
        {
            "icon": "📊",
            "title": "面试总结分析",
            "desc": "详细分析面试表现，提供针对性提升建议"
        },
        {
            "icon": "🌍",
            "title": "多语言支持",
            "desc": "支持中英法等多语言面试，满足国际品牌需求"
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{feature["icon"]}</div>
            <h3 class="feature-title">{feature["title"]}</h3>
            <p class="feature-desc">{feature["desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # 页脚
    st.markdown("""
    <div class="footer">
        <p class="footer-text">© 2024 奢华面试AI. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard_page():
    # 导航栏
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.markdown('<div class="logo"><span style="font-size:1.75rem">💎</span><span>奢华面试AI</span></div>', unsafe_allow_html=True)
    with col3:
        if st.button("返回首页", use_container_width=True):
            st.session_state.current_page = 'landing'
            st.rerun()

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    
    st.title("🎯 欢迎使用奢华面试AI")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 品牌知识库", "💬 AI面试", "📝 简历管理", "📊 面试记录"])
    
    with tab1:
        st.subheader("奢侈品知识库")
        brands = [
            ("Louis Vuitton", "法国奢侈品品牌，以精湛工艺和经典设计著称"),
            ("Chanel", "法国奢侈品牌，以优雅与简约的设计理念闻名"),
            ("Hermès", "法国奢侈品品牌，坚持手工制作和高品质传统"),
            ("Cartier", "法国珠宝和腕表品牌，被誉为\"皇帝的珠宝商\""),
            ("Gucci", "意大利奢侈品牌，以双G标志和独特风格著称")
        ]
        
        for name, desc in brands:
            with st.expander(f"💎 {name}", expanded=False):
                st.write(desc)
                st.info("更多品牌知识将持续更新...")
    
    with tab2:
        st.subheader("开始AI面试")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("选择目标品牌", ["Louis Vuitton", "Chanel", "Hermès", "Gucci", "Cartier"])
        with col2:
            st.selectbox("选择面试类型", ["品牌认知", "VIP场景模拟", "综合面试"])
        
        if st.button("开始面试", type="primary"):
            st.info("面试功能开发中...")
    
    with tab3:
        st.subheader("简历管理")
        uploaded_file = st.file_uploader("上传简历文件 (PDF/Word)", type=['pdf', 'docx', 'doc'])
        if uploaded_file:
            st.success("简历上传成功！")
            if st.button("AI优化简历"):
                st.info("简历优化功能开发中...")
    
    with tab4:
        st.subheader("面试记录")
        st.info("暂无面试记录，开始您的第一次AI面试吧！")

def render_login_modal():
    if st.session_state.show_modal in ['login', 'register']:
        st.markdown("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        ">
            <div style="
                background: linear-gradient(135deg, #0A0E27 0%, #151935 100%);
                border: 1px solid rgba(212,175,55,0.2);
                border-radius: 16px;
                padding: 2.5rem;
                max-width: 450px;
                width: 90%;
            ">
        """, unsafe_allow_html=True)
        
        is_login = st.session_state.show_modal == 'login'
        st.markdown(f'<h2 style="color: white; margin-bottom: 0.5rem;">{"登录" if is_login else "注册"}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: rgba(255,255,255,0.6); margin-bottom: 2rem;">{"欢迎回来，请登录您的账号" if is_login else "创建账号，开始您的奢侈品面试之旅"}</p>', unsafe_allow_html=True)
        
        with st.form(key=f"{st.session_state.show_modal}_form"):
            if not is_login:
                name = st.text_input("姓名", placeholder="请输入您的姓名")
                email = st.text_input("邮箱", placeholder="请输入您的邮箱")
            
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("登录" if is_login else "注册", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("取消", use_container_width=True)
            
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
                            st.success("登录成功！")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("登录失败，请检查用户名和密码")
                    except Exception as e:
                        st.error(f"无法连接到服务器：{str(e)}")
                        st.info("提示：请确保后端服务正在运行")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/register",
                            json={
                                "username": username,
                                "email": email if 'email' in locals() else "test@test.com",
                                "full_name": name if 'name' in locals() else "用户",
                                "password": password
                            }
                        )
                        if response.status_code == 200:
                            st.success("注册成功！请登录")
                            st.session_state.show_modal = 'login'
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"注册失败：{response.text}")
                    except Exception as e:
                        st.error(f"无法连接到服务器：{str(e)}")
                        st.info("提示：请确保后端服务正在运行")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# 主渲染逻辑
if st.session_state.current_page == 'landing':
    render_landing_page()
elif st.session_state.current_page == 'dashboard':
    render_dashboard_page()

if st.session_state.show_modal:
    render_login_modal()

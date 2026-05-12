import streamlit as st
import requests
import time
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="奢华面试AI - 奢侈品行业AI面试助手",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --gold-primary: #D4AF37;
        --gold-light: #F4E4BA;
        --gold-dark: #B8860B;
        --navy-dark: #0A0E27;
        --navy-medium: #151935;
        --white-pure: #FFFFFF;
        --gray-light: rgba(255,255,255,0.6);
        --gray-medium: rgba(255,255,255,0.4);
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
    
    .logo-icon {
        font-size: 1.75rem;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: rgba(255,255,255,0.8);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
        cursor: pointer;
    }
    
    .nav-link:hover {
        color: var(--gold-primary);
    }
    
    /* 按钮样式 */
    .btn-primary {
        background: linear-gradient(135deg, var(--gold-primary) 0%, var(--gold-dark) 100%);
        color: var(--navy-dark) !important;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.75rem;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.3);
    }
    
    .btn-secondary {
        background: transparent;
        border: 1px solid rgba(212, 175, 55, 0.3);
        color: var(--gold-primary);
        font-weight: 500;
        border-radius: 8px;
        padding: 0.75rem 1.75rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-secondary:hover {
        background: rgba(212, 175, 55, 0.1);
        border-color: var(--gold-primary);
    }
    
    /* 英雄区域 */
    .hero {
        padding: 5rem 2rem;
        text-align: center;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        color: var(--gold-primary);
        font-size: 0.875rem;
        margin-bottom: 1.5rem;
    }
    
    .hero-title {
        font-size: 4rem;
        color: white;
        line-height: 1.1;
        margin-bottom: 1.5rem;
    }
    
    .hero-highlight {
        background: linear-gradient(135deg, var(--gold-primary) 0%, var(--gold-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.7);
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }
    
    .hero-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 4rem;
    }
    
    /* 平台支持 */
    .section {
        padding: 5rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .section-title {
        text-align: center;
        font-size: 2rem;
        color: white;
        margin-bottom: 3rem;
    }
    
    .platforms-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1.5rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .platform-item {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .platform-item:hover {
        border-color: rgba(212, 175, 55, 0.3);
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
    
    /* 功能卡片 */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(212,175,55,0.03) 100%);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 175, 55, 0.2);
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
    
    /* 岗位分类 */
    .roles-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 3rem;
    }
    
    .role-card {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .role-card:hover, .role-card.active {
        background: rgba(212, 175, 55, 0.1);
        border-color: var(--gold-primary);
    }
    
    .role-name {
        color: white;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .role-desc {
        color: rgba(255,255,255,0.6);
        font-size: 0.875rem;
    }
    
    /* 成功案例 */
    .testimonials-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .testimonial-card {
        background: rgba(212, 175, 55, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 16px;
        padding: 2rem;
    }
    
    .testimonial-content {
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
        margin-bottom: 1.5rem;
        font-style: italic;
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .testimonial-avatar {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--gold-primary), var(--gold-dark));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .testimonial-name {
        color: white;
        font-weight: 600;
    }
    
    .testimonial-role {
        color: rgba(255,255,255,0.6);
        font-size: 0.875rem;
    }
    
    /* FAQ */
    .faq-item {
        background: rgba(212, 175, 55, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 12px;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .faq-question {
        padding: 1.5rem;
        color: white;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .faq-answer {
        padding: 0 1.5rem 1.5rem;
        color: rgba(255,255,255,0.7);
        line-height: 1.6;
    }
    
    /* CTA区域 */
    .cta-section {
        text-align: center;
        padding: 5rem 2rem;
        background: linear-gradient(180deg, transparent 0%, rgba(212,175,55,0.05) 100%);
    }
    
    .cta-title {
        font-size: 2.5rem;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    /* 页脚 */
    .footer {
        border-top: 1px solid rgba(212,175,55,0.1);
        padding: 4rem 2rem 2rem;
        margin-top: 3rem;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .footer-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .footer-desc {
        color: rgba(255,255,255,0.6);
        line-height: 1.6;
    }
    
    .footer-title {
        color: var(--gold-primary);
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    .footer-link {
        color: rgba(255,255,255,0.7);
        display: block;
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: color 0.3s;
        text-decoration: none;
    }
    
    .footer-link:hover {
        color: var(--gold-primary);
    }
    
    .footer-bottom {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(212,175,55,0.1);
        text-align: center;
        color: rgba(255,255,255,0.5);
    }
    
    /* 模态框 */
    .modal-overlay {
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
    }
    
    .modal {
        background: linear-gradient(135deg, #0A0E27 0%, #151935 100%);
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 16px;
        padding: 2.5rem;
        max-width: 450px;
        width: 90%;
    }
    
    .modal-title {
        font-size: 1.75rem;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .modal-subtitle {
        color: rgba(255,255,255,0.6);
        margin-bottom: 2rem;
    }
    
    .input-field {
        width: 100%;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(212,175,55,0.2);
        border-radius: 8px;
        padding: 0.875rem 1rem;
        color: white;
        margin-bottom: 1rem;
        font-size: 1rem;
    }
    
    .input-field:focus {
        outline: none;
        border-color: var(--gold-primary);
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

load_css()

# 初始化状态
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'token' not in st.session_state:
    st.session_state.token = None
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = None
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None
if 'expanded_faq' not in st.session_state:
    st.session_state.expanded_faq = []

API_BASE_URL = "http://localhost:8000"

# 导航栏
def render_navbar():
    st.markdown("""
    <div class="navbar">
        <div class="navbar-content">
            <div class="logo">
                <span class="logo-icon">💎</span>
                <span>奢华面试AI</span>
            </div>
            <div class="nav-links">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 4])
    with col1:
        if st.button("产品功能", key="nav_features", use_container_width=False):
            st.session_state.current_page = 'landing'
            st.rerun()
    with col2:
        if not st.session_state.token:
            if st.button("立即登录", key="nav_login", type="primary"):
                st.session_state.show_modal = 'login'
                st.rerun()
        else:
            if st.button("进入系统", key="nav_dashboard", type="primary"):
                st.session_state.current_page = 'dashboard'
                st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# 英雄区域
def render_hero():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✨ 专业奢侈品行业AI面试助手</div>
        <h1 class="hero-title">
            奢华面试AI<br>
            <span class="hero-highlight">助你轻松拿OFFER</span>
        </h1>
        <p class="hero-subtitle">
            专为奢侈品行业打造的AI面试助手<br>
            深度品牌知识 · VIP场景模拟 · 专业面试训练
        </p>
        <div class="hero-buttons">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("免费使用", type="primary", key="hero_free", use_container_width=True):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
                st.rerun()
            else:
                st.session_state.current_page = 'dashboard'
                st.rerun()
    with col2:
        if st.button("使用手册", key="hero_guide", use_container_width=True):
            pass
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# 平台支持
def render_platforms():
    platforms = [
        ("🏛️", "路易威登"),
        ("👜", "香奈儿"),
        ("👑", "爱马仕"),
        ("💍", "卡地亚"),
        ("👠", "古驰"),
        ("⌚", "劳力士"),
        ("👗", "迪奥"),
        ("💎", "宝格丽"),
        ("🎩", "普拉达"),
        ("🌸", "范思哲")
    ]
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">支持所有顶级奢侈品牌</h2>', unsafe_allow_html=True)
    st.markdown('<div class="platforms-grid">', unsafe_allow_html=True)
    
    for icon, name in platforms:
        st.markdown(f"""
        <div class="platform-item">
            <div class="platform-icon">{icon}</div>
            <div class="platform-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# 核心功能
def render_features():
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
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">奢华面试AI核心功能</h2>', unsafe_allow_html=True)
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{feature["icon"]}</div>
            <h3 class="feature-title">{feature["title"]}</h3>
            <p class="feature-desc">{feature["desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# 岗位分类
def render_roles():
    roles = [
        {
            "name": "精品销售",
            "desc": "品牌顾问、销售主管、VIP客户经理等岗位"
        },
        {
            "name": "品牌营销",
            "desc": "市场推广、品牌经理、数字营销等岗位"
        },
        {
            "name": "客户服务",
            "desc": "VIP服务、客户关系管理、售后服务等岗位"
        },
        {
            "name": "运营管理",
            "desc": "店铺运营、库存管理、供应链管理等岗位"
        },
        {
            "name": "设计创意",
            "desc": "珠宝设计、皮具设计、视觉陈列等岗位"
        },
        {
            "name": "职能支持",
            "desc": "人力资源、财务、法务等后台支持岗位"
        }
    ]
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">适用多个奢侈品岗位</h2>', unsafe_allow_html=True)
    st.markdown('<div class="roles-grid">', unsafe_allow_html=True)
    
    for idx, role in enumerate(roles):
        is_active = st.session_state.selected_role == idx
        if st.button(f"{role['name']}\n{role['desc']}", key=f"role_{idx}", 
                    use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.selected_role = idx
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 岗位详情展示
    if st.session_state.selected_role is not None:
        selected_role = roles[st.session_state.selected_role]
        st.markdown(f"""
        <div style="margin-top: 3rem; text-align: center;">
            <div class="luxury-card">
                <h3 style="color: var(--gold-primary); margin-bottom: 1rem;">{selected_role["name"]}面试助手</h3>
                <p style="color: rgba(255,255,255,0.7); margin-bottom: 1.5rem;">
                    针对{selected_role["desc"]}
                </p>
        """, unsafe_allow_html=True)
        
        if st.button("免费体验该岗位面试", type="primary", key="try_role"):
            if not st.session_state.token:
                st.session_state.show_modal = 'register'
            else:
                st.session_state.current_page = 'dashboard'
            st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# 成功案例
def render_testimonials():
    testimonials = [
        {
            "name": "陈雅琳",
            "role": "成功入职 Louis Vuitton",
            "content": "通过奢华面试AI的训练，我顺利通过了LV的三轮面试！VIP场景模拟特别实用，让我在真实面试中表现得非常专业。"
        },
        {
            "name": "Marco Wang",
            "role": "成功入职 Gucci",
            "content": "品牌知识库功能太棒了！让我对Gucci的历史有了更深入的了解，面试时聊起品牌故事让HR印象深刻。"
        },
        {
            "name": "林雨薇",
            "role": "成功入职 Cartier",
            "content": "AI简历优化让我的简历焕然一新，奢侈品化的表达让我在众多申请者中脱颖而出！"
        }
    ]
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">成功案例</h2>', unsafe_allow_html=True)
    st.markdown('<div class="testimonials-grid">', unsafe_allow_html=True)
    
    for t in testimonials:
        st.markdown(f"""
        <div class="testimonial-card">
            <p class="testimonial-content">"{t['content']}"</p>
            <div class="testimonial-author">
                <div class="testimonial-avatar">👤</div>
                <div>
                    <div class="testimonial-name">{t['name']}</div>
                    <div class="testimonial-role">{t['role']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# FAQ
def render_faq():
    faqs = [
        {
            "q": "奢华面试AI适用于什么岗位？",
            "a": "我们的AI面试助手适用于所有奢侈品行业岗位，包括精品销售、品牌营销、客户服务、运营管理、设计创意等各类岗位。"
        },
        {
            "q": "奢华面试AI可以免费试用吗？",
            "a": "是的，我们提供免费试用额度，您可以注册后立即开始体验完整的AI面试功能。"
        },
        {
            "q": "奢华面试AI支持哪些语言？",
            "a": "我们支持中文、英文、法语、日语等多种语言面试，满足国际奢侈品牌的多语言需求。"
        },
        {
            "q": "使用奢华面试AI我的信息会泄露吗？",
            "a": "我们非常重视用户隐私，所有数据都经过加密处理，您的面试记录和个人信息不会被泄露。"
        },
        {
            "q": "如何获取更多面试资源？",
            "a": "注册后您可以访问我们完整的品牌知识库、面试题库和学习资源，帮助您全方位备战。"
        }
    ]
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">常见问题</h2>', unsafe_allow_html=True)
    
    for idx, faq in enumerate(faqs):
        is_expanded = idx in st.session_state.expanded_faq
        if st.button(faq["q"], key=f"faq_{idx}", use_container_width=True):
            if idx in st.session_state.expanded_faq:
                st.session_state.expanded_faq.remove(idx)
            else:
                st.session_state.expanded_faq.append(idx)
            st.rerun()
        
        if is_expanded:
            st.markdown(f"""
            <div style="padding: 0 1.5rem 1.5rem; color: rgba(255,255,255,0.7); line-height: 1.6;">
                {faq["a"]}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# CTA区域
def render_cta():
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">用奢华面试AI，面试不再难</h2>
    """, unsafe_allow_html=True)
    
    if st.button("免费使用", type="primary", key="cta_free"):
        if not st.session_state.token:
            st.session_state.show_modal = 'register'
        else:
            st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 页脚
def render_footer():
    st.markdown("""
    <div class="footer">
        <div class="footer-grid">
            <div>
                <div class="footer-logo">💎 奢华面试AI</div>
                <p class="footer-desc">
                    专为奢侈品行业打造的AI面试助手，帮助您实现职业梦想。
                </p>
            </div>
            <div>
                <h4 class="footer-title">产品</h4>
                <div class="footer-link">AI面试助手</div>
                <div class="footer-link">品牌知识库</div>
                <div class="footer-link">AI简历优化</div>
            </div>
            <div>
                <h4 class="footer-title">资源</h4>
                <div class="footer-link">使用手册</div>
                <div class="footer-link">用户协议</div>
                <div class="footer-link">隐私政策</div>
            </div>
            <div>
                <h4 class="footer-title">联系我们</h4>
                <div class="footer-link">客服微信</div>
                <div class="footer-link">商务合作</div>
                <div class="footer-link">意见反馈</div>
            </div>
        </div>
        <div class="footer-bottom">
            © 2024 奢华面试AI. All rights reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 登录/注册模态框
def render_modal():
    if st.session_state.show_modal in ['login', 'register']:
        is_login = st.session_state.show_modal == 'login'
        
        st.markdown('<div class="modal-overlay">', unsafe_allow_html=True)
        st.markdown('<div class="modal">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <h2 class="modal-title">{'登录' if is_login else '注册'}</h2>
        <p class="modal-subtitle">{'欢迎回来，请登录您的账号' if is_login else '创建账号，开始您的奢侈品面试之旅'}</p>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"{st.session_state.show_modal}_form"):
            if not is_login:
                name = st.text_input("姓名", placeholder="请输入您的姓名")
                email = st.text_input("邮箱", placeholder="请输入您的邮箱")
            
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit_btn = st.form_submit_button("登录" if is_login else "注册", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("取消", use_container_width=True):
                    st.session_state.show_modal = None
                    st.rerun()
            
            if submit_btn:
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
                        st.error(f"登录失败: {str(e)}")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/register",
                            json={
                                "username": username,
                                "email": email,
                                "full_name": name,
                                "password": password
                            }
                        )
                        if response.status_code == 200:
                            st.success("注册成功！请登录")
                            time.sleep(1)
                            st.session_state.show_modal = 'login'
                            st.rerun()
                        else:
                            st.error(f"注册失败: {response.text}")
                    except Exception as e:
                        st.error(f"注册失败: {str(e)}")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# 仪表板页面
def render_dashboard():
    st.markdown("""
    <div class="section">
        <h2 class="section-title">欢迎使用奢华面试AI</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 品牌知识库", "💬 AI面试", "📝 简历管理", "📊 面试记录"])
    
    with tab1:
        st.markdown("""
        <div class="section">
            <h3 style="color: var(--gold-primary); margin-bottom: 1.5rem;">奢侈品知识库</h3>
        """, unsafe_allow_html=True)
        
        brands = [
            ("Louis Vuitton", "法国奢侈品品牌，以精湛工艺和经典设计著称"),
            ("Chanel", "法国奢侈品牌，以优雅与简约的设计理念闻名"),
            ("Hermès", "法国奢侈品品牌，坚持手工制作和高品质传统"),
            ("Cartier", "法国珠宝和腕表品牌，被誉为'皇帝的珠宝商'"),
            ("Gucci", "意大利奢侈品牌，以双G标志和独特风格著称")
        ]
        
        for name, desc in brands:
            with st.expander(f"💎 {name}", expanded=False):
                st.write(desc)
                st.info("更多品牌知识将持续更新...")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="section">
            <h3 style="color: var(--gold-primary); margin-bottom: 1.5rem;">开始AI面试</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.selectbox("选择目标品牌", ["Louis Vuitton", "Chanel", "Hermès", "Gucci", "Cartier"])
        with col2:
            st.selectbox("选择面试类型", ["品牌认知", "VIP场景模拟", "综合面试"])
        
        if st.button("开始面试", type="primary", key="start_interview"):
            st.info("面试功能开发中...")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="section">
            <h3 style="color: var(--gold-primary); margin-bottom: 1.5rem;">简历管理</h3>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("上传简历文件 (PDF/Word)", type=['pdf', 'docx', 'doc'])
        if uploaded_file:
            st.success("简历上传成功！")
            if st.button("AI优化简历"):
                st.info("简历优化功能开发中...")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="section">
            <h3 style="color: var(--gold-primary); margin-bottom: 1.5rem;">面试记录</h3>
        """, unsafe_allow_html=True)
        
        st.info("暂无面试记录，开始您的第一次AI面试吧！")
        
        st.markdown("</div>", unsafe_allow_html=True)

# 主渲染
render_navbar()

if st.session_state.current_page == 'landing':
    render_hero()
    render_platforms()
    render_features()
    render_roles()
    render_testimonials()
    render_faq()
    render_cta()
elif st.session_state.current_page == 'dashboard':
    render_dashboard()

render_footer()
render_modal()

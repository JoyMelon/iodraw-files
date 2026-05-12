import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="奢侈品行业AI面试助手",
    page_icon="💎",
    layout="wide"
)

# 初始化session状态
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

# 侧边栏
st.sidebar.title("💎 奢侈品面试助手")

# 用户信息显示
if st.session_state.token:
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        user_response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
        if user_response.status_code == 200:
            user = user_response.json()
            st.sidebar.success(f"欢迎, {user.get('full_name', user['username'])}!")
    except:
        pass

# 导航
if st.session_state.token:
    page = st.sidebar.radio(
        "导航",
        ["📄 职位发布", "📝 简历管理", "🎯 AI面试", "📊 面试记录"]
    )
    # 页面映射
    page_map = {
        "📄 职位发布": "jobs",
        "📝 简历管理": "resumes",
        "🎯 AI面试": "interview",
        "📊 面试记录": "history"
    }
    st.session_state.current_page = page_map[page]
    
    if st.sidebar.button("退出登录"):
        st.session_state.token = None
        st.session_state.current_page = 'welcome'
        st.rerun()
else:
    st.session_state.current_page = 'welcome'

# 欢迎页面（登录/注册）
if st.session_state.current_page == 'welcome':
    st.title("💎 奢侈品行业AI面试助手")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("登录")
        login_username = st.text_input("用户名", key="login_user")
        login_password = st.text_input("密码", type="password", key="login_pass")
        
        if st.button("登录", type="primary"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/token",
                    data={"username": login_username, "password": login_password}
                )
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    st.success("登录成功!")
                    st.session_state.current_page = 'jobs'
                    st.rerun()
                else:
                    st.error("登录失败，请检查用户名和密码")
            except Exception as e:
                st.error(f"登录失败: {e}")
    
    with col2:
        st.header("注册")
        reg_username = st.text_input("用户名", key="reg_user")
        reg_email = st.text_input("邮箱", key="reg_email")
        reg_fullname = st.text_input("姓名", key="reg_name")
        reg_password = st.text_input("密码", type="password", key="reg_pass")
        
        if st.button("注册"):
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
                    st.success("注册成功，请登录!")
                else:
                    st.error(f"注册失败: {response.text}")
            except Exception as e:
                st.error(f"注册失败: {e}")

# 职位发布页面
elif st.session_state.current_page == 'jobs':
    st.title("📄 职位信息")
    st.markdown("---")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # 发布新职位
    st.subheader("发布新职位")
    with st.form("post_job_form"):
        job_title = st.text_input("职位名称")
        job_company = st.text_input("公司名称")
        job_brand = st.selectbox("目标品牌", ["路易威登", "香奈儿", "爱马仕", "古驰", "卡地亚", "其他"])
        job_location = st.text_input("工作地点")
        job_description = st.text_area("职位描述")
        job_requirements = st.text_area("任职要求")
        
        submitted = st.form_submit_button("发布职位")
        if submitted:
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
                    st.success("职位发布成功!")
                else:
                    st.error(f"发布失败: {response.text}")
            except Exception as e:
                st.error(f"发布失败: {e}")
    
    st.markdown("---")
    
    # 显示现有职位
    st.subheader("可用职位")
    
    try:
        # 获取现有职位
        jobs_response = requests.get(f"{API_BASE_URL}/jobs/legacy", headers=headers)
        if jobs_response.status_code == 200:
            jobs = jobs_response.json()
            if jobs:
                for job in jobs:
                    with st.expander(f"{job['company']} - {job['position']}"):
                        st.write(f"**公司:** {job['company']}")
                        st.write(f"**职位:** {job['position']}")
                        st.write(f"**要求:** {job['requirement']}")
                        if job.get('description'):
                            st.write(f"**描述:** {job['description']}")
            else:
                st.info("暂无职位信息")
    except Exception as e:
        st.error(f"获取职位失败: {e}")

# 简历管理页面
elif st.session_state.current_page == 'resumes':
    st.title("📝 简历管理")
    st.markdown("---")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # 上传简历
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("上传简历文件")
        uploaded_file = st.file_uploader("选择简历文件", type=['pdf', 'docx', 'doc', 'txt'])
        
        if uploaded_file and st.button("上传并解析"):
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
                        st.success("简历上传成功!")
                        st.session_state.selected_resume_id = result['resume_id']
                        
                        # 显示优化建议
                        st.subheader("💡 优化建议")
                        st.write(result['optimization_suggestions'])
                        
                        st.subheader("✨ 奢侈品行业版本")
                        st.write(result['luxury_version'])
                        st.rerun()
                    else:
                        st.error(f"上传失败: {response.text}")
                except Exception as e:
                    st.error(f"上传失败: {e}")
    
    with col2:
        st.subheader("或粘贴简历内容")
        resume_name = st.text_input("简历名称（您的姓名）")
        resume_text = st.text_area("粘贴简历内容", height=200)
        
        if st.button("提交简历") and resume_name and resume_text:
            with st.spinner("正在处理简历..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/upload/resume/text",
                        data={"name": resume_name, "resume_text": resume_text},
                        headers=headers
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("简历提交成功!")
                        st.session_state.selected_resume_id = result['resume_id']
                        
                        st.subheader("💡 优化建议")
                        st.write(result['optimization_suggestions'])
                        
                        st.subheader("✨ 奢侈品行业版本")
                        st.write(result['luxury_version'])
                        st.rerun()
                    else:
                        st.error(f"提交失败: {response.text}")
                except Exception as e:
                    st.error(f"提交失败: {e}")
    
    st.markdown("---")
    
    # 显示已上传的简历
    st.subheader("我的简历")
    try:
        resumes_response = requests.get(f"{API_BASE_URL}/resumes", headers=headers)
        if resumes_response.status_code == 200:
            resumes = resumes_response.json()
            if resumes:
                for resume in resumes:
                    with st.expander(f"{resume['name']} (评分: {resume['score']:.1f}/10)"):
                        st.write(f"**上传时间:** {resume['created_at']}")
                        if resume.get('original_filename'):
                            st.write(f"**文件:** {resume['original_filename']}")
                        
                        if st.button(f"选择此简历进行面试", key=f"select_resume_{resume['id']}"):
                            st.session_state.selected_resume_id = resume['id']
                            st.success("简历已选择!")
                        
                        if resume.get('optimization_suggestions'):
                            st.subheader("优化建议")
                            st.write(resume['optimization_suggestions'])
                        
                        if resume.get('luxury_translated_version'):
                            st.subheader("奢侈品版本")
                            st.write(resume['luxury_translated_version'])
            else:
                st.info("您还没有上传简历")
    except Exception as e:
        st.error(f"获取简历失败: {e}")

# AI面试页面
elif st.session_state.current_page == 'interview':
    st.title("🎯 AI面试")
    st.markdown("---")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # 面试准备
    if not st.session_state.current_interview_id:
        st.subheader("开始面试")
        
        # 选择简历
        try:
            resumes_response = requests.get(f"{API_BASE_URL}/resumes", headers=headers)
            resumes = resumes_response.json() if resumes_response.status_code == 200 else []
            
            if resumes:
                resume_options = {f"{r['name']} (评分: {r['score']:.1f})": r['id'] for r in resumes}
                selected_resume_label = st.selectbox("选择简历", list(resume_options.keys()))
                selected_resume_id = resume_options[selected_resume_label]
            else:
                st.warning("请先上传简历")
                st.stop()
        except Exception as e:
            st.error(f"获取简历失败: {e}")
            st.stop()
        
        # 选择职位
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
            st.error(f"获取职位失败: {e}")
            st.stop()
        
        if st.button("开始面试", type="primary"):
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
                        st.error(f"开始面试失败: {response.text}")
                except Exception as e:
                    st.error(f"开始面试失败: {e}")
    
    # 面试进行中
    else:
        st.subheader("面试进行中")
        
        # 显示当前问题
        if st.session_state.current_question:
            st.info(f"**问题:** {st.session_state.current_question}")
            
            answer = st.text_area("您的回答", height=150)
            
            if st.button("提交回答", type="primary"):
                with st.spinner("AI正在分析..."):
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
                            
                            # 记录历史
                            st.session_state.interview_history.append({
                                "question": st.session_state.current_question,
                                "answer": answer,
                                "analysis": result['analysis']
                            })
                            
                            # 显示分析
                            analysis = result['analysis']
                            st.subheader("AI分析结果")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("品牌匹配度", f"{analysis['brand_match_score']:.1f}/10")
                            with col2:
                                st.metric("语气优雅度", f"{analysis['tone_score']:.1f}/10")
                            with col3:
                                st.metric("情绪评分", f"{analysis['emotion_score']:.1f}/10")
                            
                            st.write(analysis['ai_analysis'])
                            
                            if result['interview_complete']:
                                st.success(f"🎉 面试完成! 总分: {result['total_score']:.1f}/10")
                                st.session_state.current_interview_id = None
                                st.session_state.current_question = None
                            else:
                                st.session_state.current_question = result['next_question']
                                st.rerun()
                        else:
                            st.error(f"提交失败: {response.text}")
                    except Exception as e:
                        st.error(f"提交失败: {e}")
        
        # 显示历史
        if st.session_state.interview_history:
            st.subheader("面试历史")
            for i, item in enumerate(st.session_state.interview_history):
                with st.expander(f"问题 {i+1}"):
                    st.write(f"**Q:** {item['question']}")
                    st.write(f"**A:** {item['answer']}")

# 面试记录页面
elif st.session_state.current_page == 'history':
    st.title("📊 面试记录")
    st.markdown("---")
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    try:
        interviews_response = requests.get(f"{API_BASE_URL}/interviews", headers=headers)
        if interviews_response.status_code == 200:
            interviews = interviews_response.json()
            if interviews:
                for interview in interviews:
                    status_color = {
                        "waiting": "🟡",
                        "answering": "🟢",
                        "resolved": "🔵"
                    }.get(interview['status'], "⚪")
                    
                    with st.expander(f"{status_color} 面试 #{interview['id']} - 评分: {interview['score']:.1f}/10"):
                        st.write(f"**状态:** {interview['status']}")
                        st.write(f"**时间:** {interview['created_at']}")
                        
                        # 获取面试详情
                        try:
                            detail_response = requests.get(
                                f"{API_BASE_URL}/interview/{interview['id']}",
                                headers=headers
                            )
                            if detail_response.status_code == 200:
                                detail = detail_response.json()
                                if 'rounds' in detail and detail['rounds']:
                                    st.subheader("面试问题")
                                    for round in detail['rounds']:
                                        st.write(f"**Q:** {round['question']}")
                                        if round.get('user_answer'):
                                            st.write(f"**A:** {round['user_answer']}")
                                            st.write(f"品牌匹配: {round['brand_match_score']:.1f}, 语气: {round['tone_score']:.1f}")
                                        st.write("---")
                        except:
                            pass
            else:
                st.info("暂无面试记录")
    except Exception as e:
        st.error(f"获取面试记录失败: {e}")

import streamlit as st
import requests
import json
from typing import Dict, List

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="奢侈品行业AI面试助手",
    page_icon="💎",
    layout="wide"
)

st.title("💎 奢侈品行业AI面试助手")
st.markdown("---")

if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'resume_id' not in st.session_state:
    st.session_state.resume_id = None
if 'job_id' not in st.session_state:
    st.session_state.job_id = None
if 'interview_id' not in st.session_state:
    st.session_state.interview_id = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'interview_history' not in st.session_state:
    st.session_state.interview_history = []

col1, col2 = st.columns([3, 2])

with col2:
    st.subheader("📋 岗位详情")
    
    try:
        jobs_response = requests.get(f"{API_BASE_URL}/api/jobs")
        if jobs_response.status_code == 200:
            jobs = jobs_response.json()
            if jobs:
                job_options = {f"{job['company']} - {job['position']}": job['id'] for job in jobs}
                selected_job = st.selectbox("选择面试岗位", list(job_options.keys()))
                st.session_state.job_id = job_options[selected_job]
                
                selected_job_data = next(job for job in jobs if job['id'] == st.session_state.job_id)
                st.markdown(f"**公司:** {selected_job_data['company']}")
                st.markdown(f"**职位:** {selected_job_data['position']}")
                st.markdown(f"**要求:** {selected_job_data['requirement']}")
            else:
                st.info("暂无岗位信息")
    except Exception as e:
        st.error(f"无法连接到后端服务: {e}")
    
    st.subheader("👤 简历信息")
    if st.session_state.resume_id:
        st.success("简历已上传！")
    else:
        st.info("请先上传简历")

with col1:
    if st.session_state.current_step == 0:
        st.subheader("第一步：上传您的简历")
        
        resume_text = st.text_area(
            "请输入您的简历内容（或粘贴在此）",
            height=200,
            placeholder="姓名：张三\n教育背景：XX大学\n工作经验：XX公司XX职位...\n技能：沟通、销售、客户服务..."
        )
        name = st.text_input("您的姓名")
        
        if st.button("上传并解析简历", type="primary"):
            if resume_text and name:
                with st.spinner("正在解析简历..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/api/resume/upload",
                            json={"resume_text": resume_text, "name": name}
                        )
                        if response.status_code == 200:
                            resume_data = response.json()
                            st.session_state.resume_id = resume_data['id']
                            
                            st.success("简历解析成功！")
                            st.subheader("奢侈品化简历版本")
                            st.write(resume_data['luxury_translated_version'])
                            st.subheader("推荐品牌")
                            st.write("根据您的简历，我们推荐以下品牌：Louis Vuitton, Chanel, Hermès")
                            st.session_state.current_step = 1
                            st.rerun()
                        else:
                            st.error("简历上传失败")
                    except Exception as e:
                        st.error(f"错误: {e}")
            else:
                st.warning("请填写简历内容和姓名")
    
    elif st.session_state.current_step == 1:
        st.subheader("第二步：开始面试")
        
        if st.button("开始AI面试", type="primary"):
            if st.session_state.job_id and st.session_state.resume_id:
                with st.spinner("正在准备面试..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/api/interview/start",
                            json={
                                "user_id": 1,
                                "job_id": st.session_state.job_id,
                                "resume_id": st.session_state.resume_id
                            }
                        )
                        if response.status_code == 200:
                            interview_data = response.json()
                            st.session_state.interview_id = interview_data['id']
                            
                            if interview_data['rounds']:
                                st.session_state.current_question = interview_data['rounds'][0]['question']
                            
                            st.session_state.current_step = 2
                            st.success("面试已开始！")
                            st.rerun()
                        else:
                            st.error("面试启动失败")
                    except Exception as e:
                        st.error(f"错误: {e}")
            else:
                st.warning("请先选择岗位和上传简历")
    
    elif st.session_state.current_step == 2:
        st.subheader("第三步：面试进行中")
        
        if st.session_state.current_question:
            st.info(f"**问题:** {st.session_state.current_question}")
            
            answer = st.text_area("您的回答", height=150, placeholder="请输入您的回答...")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("提交回答", type="primary"):
                    if answer:
                        with st.spinner("AI正在分析您的回答..."):
                            try:
                                response = requests.post(
                                    f"{API_BASE_URL}/api/interview/answer",
                                    json={
                                        "interview_id": st.session_state.interview_id,
                                        "answer": answer
                                    }
                                )
                                if response.status_code == 200:
                                    result = response.json()
                                    
                                    st.session_state.interview_history.append({
                                        "question": st.session_state.current_question,
                                        "answer": answer,
                                        "analysis": result['analysis']
                                    })
                                    
                                    st.subheader("AI分析结果")
                                    
                                    col1_score, col2_score = st.columns(2)
                                    with col1_score:
                                        st.metric("品牌匹配度", f"{result['analysis']['brand_match_score']}/10")
                                    with col2_score:
                                        st.metric("语气优雅度", f"{result['analysis']['tone_score']}/10")
                                    
                                    st.write(result['analysis']['ai_analysis'])
                                    st.write(f"💡 {result['analysis']['tone_feedback']}")
                                    
                                    if result['interview_complete']:
                                        st.success("🎉 面试已完成！")
                                        st.session_state.current_step = 3
                                    else:
                                        st.session_state.current_question = result['next_question']
                                    
                                    st.rerun()
                                else:
                                    st.error("提交失败")
                            except Exception as e:
                                st.error(f"错误: {e}")
                    else:
                        st.warning("请输入您的回答")
            
            with col_b:
                st.button("🎤 语音输入（功能开发中）", disabled=True)
        
        if st.session_state.interview_history:
            st.subheader("📝 面试历史")
            for i, item in enumerate(reversed(st.session_state.interview_history)):
                with st.expander(f"问题 {len(st.session_state.interview_history) - i}"):
                    st.markdown(f"**问:** {item['question']}")
                    st.markdown(f"**答:** {item['answer']}")
    
    elif st.session_state.current_step == 3:
        st.subheader("🎉 面试完成！")
        st.success("恭喜您完成了本次AI面试！")
        
        if st.session_state.interview_history:
            st.subheader("📊 面试回顾")
            for i, item in enumerate(st.session_state.interview_history):
                with st.expander(f"问题 {i + 1}", expanded=True):
                    st.markdown(f"**问:** {item['question']}")
                    st.markdown(f"**答:** {item['answer']}")
        
        if st.button("重新开始面试"):
            st.session_state.current_step = 0
            st.session_state.resume_id = None
            st.session_state.interview_id = None
            st.session_state.current_question = None
            st.session_state.interview_history = []
            st.rerun()

st.sidebar.title("💎 关于")
st.sidebar.info(
    "这是一个专为奢侈品行业设计的AI面试助手，\n"
    "帮助您准备LV、Chanel、Hermès等品牌的面试。\n\n"
    "特色功能：\n"
    "• 品牌知识库问答\n"
    "• VIP客户场景模拟\n"
    "• 语气优雅度评估\n"
    "• 简历奢侈品化改写"
)

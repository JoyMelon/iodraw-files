from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import os
import uuid
import random

from . import models, schemas, auth, database
from .resume_parser import ResumeParser
from .interview_engine import InterviewEngine
from .luxury_knowledge_rag_simple import LuxuryKnowledgeRAG
from .file_parser import FileParser

# 创建数据库表
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="奢侈品行业AI面试助手", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
rag_system = LuxuryKnowledgeRAG()
interview_engine = InterviewEngine()
resume_parser = ResumeParser()
file_parser = FileParser()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        # 初始化示例职位
        sample_jd = models.JobDescription(
            company="LVMH",
            position="精品店销售顾问",
            requirement="要求形象气质佳，有高端品牌销售经验，具备良好的沟通能力和客户服务意识",
            description="负责店内精品销售、VIP客户维护、品牌形象展示",
            target_brand_ids="1,2"
        )
        if not db.query(models.JobDescription).filter_by(company="LVMH").first():
            db.add(sample_jd)
            db.commit()
    finally:
        db.close()

SessionLocal = database.SessionLocal

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user

# 文件上传和简历处理
@app.post("/upload/resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    file_extension = file.filename.split('.')[-1].lower()
    valid_extensions = ['pdf', 'docx', 'doc', 'txt']
    
    if file_extension not in valid_extensions:
        raise HTTPException(status_code=400, detail="File type not supported")
    
    # 保存文件
    file_id = str(uuid.uuid4())
    file_path = f"./data/uploads/{file_id}.{file_extension}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 解析文件
    parsed_content = file_parser.parse_file(file_path, file_extension)
    
    # 提取简历信息
    resume_info = file_parser.extract_resume_info(parsed_content)
    
    # 生成优化建议和奢侈品版本
    optimization_suggestions = file_parser.generate_optimization_suggestions(parsed_content)
    luxury_version = file_parser.translate_to_luxury_terms(parsed_content)
    
    # 保存到数据库
    db_resume = models.Resume(
        user_id=current_user.id,
        original_filename=file.filename,
        file_path=file_path,
        file_type=file_extension,
        name=resume_info['name'],
        skills=resume_info['skills'],
        experience=resume_info['experience'],
        education=resume_info['education'],
        summary=resume_info['summary'],
        parsed_content=resume_info['parsed_content'],
        luxury_translated_version=luxury_version,
        optimization_suggestions=optimization_suggestions,
        score=random.uniform(7.0, 9.5),
        is_processed=True
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return {
        "resume_id": db_resume.id,
        "message": "Resume uploaded and processed successfully",
        "optimization_suggestions": optimization_suggestions,
        "luxury_version": luxury_version
    }

@app.post("/upload/resume/text")
async def upload_resume_text(
    name: str = Form(...),
    resume_text: str = Form(...),
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    # 提取简历信息
    resume_info = file_parser.extract_resume_info(resume_text)
    
    # 生成优化建议和奢侈品版本
    optimization_suggestions = file_parser.generate_optimization_suggestions(resume_text)
    luxury_version = file_parser.translate_to_luxury_terms(resume_text)
    
    # 保存到数据库
    db_resume = models.Resume(
        user_id=current_user.id,
        name=name,
        skills=resume_info['skills'],
        experience=resume_info['experience'],
        education=resume_info['education'],
        summary=resume_info['summary'],
        parsed_content=resume_text,
        luxury_translated_version=luxury_version,
        optimization_suggestions=optimization_suggestions,
        score=random.uniform(7.0, 9.5),
        is_processed=True
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return {
        "resume_id": db_resume.id,
        "message": "Resume uploaded and processed successfully",
        "optimization_suggestions": optimization_suggestions,
        "luxury_version": luxury_version
    }

@app.get("/resumes")
async def get_my_resumes(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    resumes = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).all()
    return resumes

@app.get("/resumes/{resume_id}")
async def get_resume(
    resume_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    resume = db.query(models.Resume).filter(
        models.Resume.id == resume_id,
        models.Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

# 职位上传功能
@app.post("/jobs/post")
async def post_job(
    job: schemas.JobPostingCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    db_job = models.JobPosting(
        user_id=current_user.id,
        title=job.title,
        company=job.company,
        description=job.description,
        requirements=job.requirements,
        brand=job.brand,
        location=job.location
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs")
async def get_jobs(
    db: Session = Depends(database.get_db)
):
    jobs = db.query(models.JobPosting).filter(models.JobPosting.is_active == True).all()
    return jobs

@app.get("/jobs/legacy")
async def get_legacy_jobs(db: Session = Depends(database.get_db)):
    return db.query(models.JobDescription).all()

# 面试相关API
@app.post("/interview/start")
async def start_interview(
    resume_id: int,
    job_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    
    if not job or not resume:
        raise HTTPException(status_code=404, detail="Job or Resume not found")
    
    interview = models.Interview(
        user_id=current_user.id,
        job_id=job_id,
        resume_id=resume_id,
        status="answering"
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    
    brand_knowledge = rag_system.query_brand_knowledge(job.requirement)
    question_data = interview_engine.generate_interview_question(
        job.requirement,
        resume.summary or "",
        brand_knowledge
    )
    
    db_round = models.Round(
        interview_id=interview.id,
        question=question_data["question"]
    )
    db.add(db_round)
    db.commit()
    
    return {
        "interview_id": interview.id,
        "question": question_data["question"],
        "status": "answering"
    }

@app.post("/interview/answer")
async def submit_answer(
    interview_id: int,
    answer: str,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id,
        models.Interview.user_id == current_user.id
    ).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    current_round = db.query(models.Round).filter(
        models.Round.interview_id == interview.id,
        models.Round.user_answer.is_(None)
    ).first()
    
    if not current_round:
        raise HTTPException(status_code=400, detail="No active question found")
    
    job = db.query(models.JobDescription).filter(models.JobDescription.id == interview.job_id).first()
    brand_knowledge = rag_system.query_brand_knowledge(job.requirement)
    
    question_data = {"type": "general", "question": current_round.question}
    analysis = interview_engine.analyze_answer(answer, question_data, brand_knowledge)
    
    current_round.user_answer = answer
    current_round.ai_analysis = analysis["ai_analysis"]
    current_round.emotion_score = analysis["emotion_score"]
    current_round.brand_match_score = analysis["brand_match_score"]
    current_round.tone_score = analysis["tone_score"]
    
    total_rounds = db.query(models.Round).filter(models.Round.interview_id == interview.id).count()
    
    next_question = None
    if total_rounds >= 3:
        interview.status = "resolved"
        total_score = (
            (current_round.brand_match_score + current_round.tone_score + current_round.emotion_score) / 3
        )
        interview.score = total_score
        interview.feedback = analysis["ai_analysis"]
    else:
        next_question_data = interview_engine.generate_interview_question(
            job.requirement,
            "",
            brand_knowledge
        )
        next_round = models.Round(
            interview_id=interview.id,
            question=next_question_data["question"]
        )
        db.add(next_round)
        next_question = next_question_data["question"]
    
    db.commit()
    
    return {
        "analysis": analysis,
        "interview_complete": total_rounds >= 3,
        "next_question": next_question,
        "total_score": interview.score if total_rounds >= 3 else None
    }

@app.get("/interview/{interview_id}")
async def get_interview(
    interview_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id,
        models.Interview.user_id == current_user.id
    ).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@app.get("/interviews")
async def get_my_interviews(
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    interviews = db.query(models.Interview).filter(
        models.Interview.user_id == current_user.id
    ).order_by(models.Interview.created_at.desc()).all()
    return interviews

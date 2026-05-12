from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import os

from . import models, schemas
from .resume_parser import ResumeParser
from .interview_engine import InterviewEngine
from .luxury_knowledge_rag import LuxuryKnowledgeRAG

DATABASE_URL = "sqlite:///./data/luxury_interview.db"
os.makedirs("./data", exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="奢侈品行业AI面试助手", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resume_parser = ResumeParser()
interview_engine = InterviewEngine()
rag_system = LuxuryKnowledgeRAG()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    rag_system.initialize_sample_data()
    db = SessionLocal()
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
    db.close()

@app.post("/api/resume/upload", response_model=schemas.Resume)
async def upload_resume(request: schemas.ResumeUploadRequest, db: Session = Depends(get_db)):
    parsed_data = resume_parser.parse_resume(request.resume_text)
    
    db_resume = models.Resume(
        name=request.name,
        skills=parsed_data["skills"],
        experience=parsed_data["experience"],
        education=parsed_data["education"],
        summary=parsed_data["summary"],
        luxury_translated_version=parsed_data["luxury_translated_version"],
        score=parsed_data["score"]
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return db_resume

@app.post("/api/interview/start", response_model=schemas.Interview)
async def start_interview(request: schemas.InterviewStartRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        user = models.User(name="候选人", email="candidate@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        request.user_id = user.id
    
    job = db.query(models.JobDescription).filter(models.JobDescription.id == request.job_id).first()
    resume = db.query(models.Resume).filter(models.Resume.id == request.resume_id).first()
    
    if not job or not resume:
        raise HTTPException(status_code=404, detail="Job or Resume not found")
    
    interview = models.Interview(
        user_id=request.user_id,
        job_id=request.job_id,
        resume_id=request.resume_id,
        status=models.InterviewStatus.waiting
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
    interview.status = models.InterviewStatus.answering
    db.commit()
    db.refresh(interview)
    
    return interview

@app.post("/api/interview/answer")
async def submit_answer(request: schemas.InterviewAnswerRequest, db: Session = Depends(get_db)):
    interview = db.query(models.Interview).filter(models.Interview.id == request.interview_id).first()
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
    analysis = interview_engine.analyze_answer(request.answer, question_data, brand_knowledge)
    
    current_round.user_answer = request.answer
    current_round.ai_analysis = analysis["ai_analysis"]
    current_round.emotion_score = analysis["emotion_score"]
    current_round.brand_match_score = analysis["brand_match_score"]
    current_round.tone_score = analysis["tone_score"]
    
    total_rounds = db.query(models.Round).filter(models.Round.interview_id == interview.id).count()
    
    if total_rounds >= 3:
        interview.status = models.InterviewStatus.resolved
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
    
    db.commit()
    
    return {
        "analysis": analysis,
        "interview_complete": total_rounds >= 3,
        "next_question": None if total_rounds >= 3 else next_question_data["question"]
    }

@app.get("/api/interview/{interview_id}", response_model=schemas.Interview)
async def get_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@app.get("/api/job/{job_id}", response_model=schemas.JobDescription)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/jobs", response_model=List[schemas.JobDescription])
async def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.JobDescription).all()

@app.post("/api/jobs", response_model=schemas.JobDescription)
async def create_job(job: schemas.JobDescriptionCreate, db: Session = Depends(get_db)):
    db_job = models.JobDescription(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/api/brands", response_model=List[schemas.LuxuryBrand])
async def list_brands(db: Session = Depends(get_db)):
    return db.query(models.LuxuryBrand).all()

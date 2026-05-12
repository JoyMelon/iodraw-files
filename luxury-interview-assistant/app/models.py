from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class InterviewStatus(enum.Enum):
    waiting = "waiting"
    answering = "answering"
    resolved = "resolved"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")
    job_postings = relationship("JobPosting", back_populates="user", cascade="all, delete-orphan")

class LuxuryBrand(Base):
    __tablename__ = "luxury_brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    founding_story = Column(Text)
    signature_product = Column(Text)
    beliefs = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    requirement = Column(Text, nullable=False)
    description = Column(Text)
    target_brand_ids = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interviews = relationship("Interview", back_populates="job")

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    company = Column(String(200))
    description = Column(Text)
    requirements = Column(Text)
    brand = Column(String(100))
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="job_postings")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_filename = Column(String(255))
    file_path = Column(String(500))
    file_type = Column(String(50))  # pdf, docx, txt
    name = Column(String(100), nullable=False)
    skills = Column(Text)
    experience = Column(Text)
    education = Column(Text)
    summary = Column(Text)
    parsed_content = Column(Text)
    luxury_translated_version = Column(Text)
    optimization_suggestions = Column(Text)
    score = Column(Float, default=0.0)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="resumes")
    interviews = relationship("Interview", back_populates="resume")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    status = Column(String(50), default="waiting")
    score = Column(Float, default=0.0)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="interviews")
    job = relationship("JobDescription", back_populates="interviews")
    resume = relationship("Resume", back_populates="interviews")
    rounds = relationship("Round", back_populates="interview", cascade="all, delete-orphan")

class Round(Base):
    __tablename__ = "rounds"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question = Column(Text, nullable=False)
    user_answer = Column(Text)
    ai_analysis = Column(Text)
    emotion_score = Column(Float, default=0.0)
    brand_match_score = Column(Float, default=0.0)
    tone_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interview = relationship("Interview", back_populates="rounds")

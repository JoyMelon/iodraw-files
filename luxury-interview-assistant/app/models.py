from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum as SQLEnum
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
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(50), default="candidate")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interviews = relationship("Interview", back_populates="user")

class LuxuryBrand(Base):
    __tablename__ = "luxury_brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    founding_story = Column(Text)
    signature_product = Column(Text)
    beliefs = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    job_descriptions = relationship("JobDescription", back_populates="target_brands")

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
    target_brands = relationship("LuxuryBrand", back_populates="job_descriptions")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    skills = Column(Text)
    experience = Column(Text)
    education = Column(Text)
    score = Column(Float, default=0.0)
    summary = Column(Text)
    luxury_translated_version = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interviews = relationship("Interview", back_populates="resume")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    status = Column(SQLEnum(InterviewStatus), default=InterviewStatus.waiting)
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

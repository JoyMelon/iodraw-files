from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LuxuryBrandBase(BaseModel):
    name: str
    description: Optional[str] = None
    founding_story: Optional[str] = None
    signature_product: Optional[str] = None
    beliefs: Optional[str] = None

class LuxuryBrandCreate(LuxuryBrandBase):
    pass

class LuxuryBrand(LuxuryBrandBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class JobDescriptionBase(BaseModel):
    company: str
    position: str
    requirement: str
    description: Optional[str] = None
    target_brand_ids: Optional[str] = None

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescription(JobDescriptionBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class JobPostingBase(BaseModel):
    title: str
    company: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    brand: Optional[str] = None
    location: Optional[str] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class ResumeBase(BaseModel):
    name: str
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    summary: Optional[str] = None

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int
    user_id: int
    original_filename: Optional[str] = None
    file_type: Optional[str] = None
    parsed_content: Optional[str] = None
    luxury_translated_version: Optional[str] = None
    optimization_suggestions: Optional[str] = None
    score: float
    is_processed: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class RoundBase(BaseModel):
    question: str
    user_answer: Optional[str] = None
    ai_analysis: Optional[str] = None
    emotion_score: Optional[float] = 0.0
    brand_match_score: Optional[float] = 0.0
    tone_score: Optional[float] = 0.0

class RoundCreate(RoundBase):
    pass

class Round(RoundBase):
    id: int
    interview_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class InterviewBase(BaseModel):
    user_id: int
    job_id: int
    resume_id: int

class InterviewCreate(InterviewBase):
    pass

class Interview(InterviewBase):
    id: int
    status: str
    score: float
    feedback: Optional[str] = None
    created_at: datetime
    rounds: List[Round] = []
    
    class Config:
        orm_mode = True

class ResumeUploadRequest(BaseModel):
    resume_text: Optional[str] = None
    name: str

class InterviewStartRequest(BaseModel):
    user_id: int
    job_id: int
    resume_id: int

class InterviewAnswerRequest(BaseModel):
    interview_id: int
    answer: str
    audio_data: Optional[str] = None

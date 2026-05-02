from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from backend.db.base import Base


class QuestionResponse(Base):
    __tablename__ = "question_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False, index=True)
    question_key = Column(String(40), nullable=False)
    question_text = Column(Text, nullable=False)
    transcript = Column(Text, nullable=False, default="")
    order_index = Column(Integer, nullable=False, default=1)
    relevance_score = Column(Float, nullable=True)
    completeness_score = Column(Float, nullable=True)
    clarity_score = Column(Float, nullable=True)
    skill_confidence_score = Column(Float, nullable=True)
    asr_confidence = Column(Float, nullable=True)
    llm_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

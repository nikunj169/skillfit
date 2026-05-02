from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON
from sqlalchemy.sql import func

from backend.db.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, index=True)
    clarity_score = Column(Float, nullable=False, default=0.0)
    confidence_score = Column(Float, nullable=False, default=0.0)
    relevance_score = Column(Float, nullable=False, default=0.0)
    overall_score = Column(Float, nullable=False, default=0.0)
    strengths = Column(JSON, nullable=False, default=list)
    improvement_areas = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

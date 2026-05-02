from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String
from sqlalchemy.sql import func

from backend.db.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    district = Column(String(80), nullable=False)
    role_applied = Column(String(120), nullable=False)
    language = Column(String(10), nullable=False, default="en")
    phone_number = Column(String(30), nullable=True)
    workforce_category = Column(String(60), nullable=False, default="SEMI_SKILLED")
    fitment_label = Column(String(60), nullable=False, default="REQUIRES_MANUAL_VERIFICATION")
    overall_score = Column(Float, nullable=False, default=0.0)
    confidence_score = Column(Float, nullable=False, default=0.0)
    integrity_flags = Column(JSON, nullable=False, default=list)
    status = Column(String(40), nullable=False, default="pending")
    shortlisted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

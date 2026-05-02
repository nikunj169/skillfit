from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.sql import func

from backend.db.base import Base


class CandidateEmbedding(Base):
    __tablename__ = "candidate_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, index=True)
    vector = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

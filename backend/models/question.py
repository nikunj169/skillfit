from sqlalchemy import Column, Integer, String, Text

from backend.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(120), nullable=False, index=True)
    language = Column(String(10), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_audio_url = Column(String(255), nullable=True)
    order_index = Column(Integer, nullable=False, default=1)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.db.base import Base
from backend.db.session import engine
from backend.models.assessment import Assessment
from backend.models.candidate import Candidate
from backend.models.embedding import CandidateEmbedding
from backend.models.question import Question
from backend.models.question_response import QuestionResponse
from backend.models.session import InterviewSession
from backend.routers import admin, assessment, classification, integrity, interview

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router, prefix=settings.api_prefix)
app.include_router(assessment.router, prefix=settings.api_prefix)
app.include_router(integrity.router, prefix=settings.api_prefix)
app.include_router(classification.router, prefix=settings.api_prefix)
app.include_router(admin.router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"message": "SkillFit backend is running."}


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}

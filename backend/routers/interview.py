import secrets

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.orm import Session
import os

from backend.dependencies import get_db
from backend.models.candidate import Candidate
from backend.models.question_response import QuestionResponse
from backend.models.session import InterviewSession
from backend.schemas.interview import (
    InterviewFinalizeRequest,
    InterviewFinalizeResponse,
    InterviewChunkSubmitResponse,
    InterviewQuestion,
    InterviewQuestionSetResponse,
    InterviewSessionStartRequest,
    InterviewSessionStartResponse,
    InterviewStatusResponse,
)
from backend.services.asr.asr_router import transcribe
from backend.services.questions import get_questions, infer_workforce_category
from backend.tasks.async_pipeline import run_interview_pipeline

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/session/start", response_model=InterviewSessionStartResponse)
def start_session(payload: InterviewSessionStartRequest, db: Session = Depends(get_db)):
    candidate = Candidate(
        **payload.model_dump(),
        workforce_category=infer_workforce_category(payload.role_applied),
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    session = InterviewSession(
        candidate_id=candidate.id,
        session_token=secrets.token_hex(16),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    questions = get_questions(payload.role_applied, payload.language, db=db)

    return InterviewSessionStartResponse(
        candidate_id=candidate.id,
        session_id=session.id,
        session_token=session.session_token,
        message="Interview session created successfully.",
        first_question=questions[0]["text"],
        total_questions=len(questions),
    )


@router.post("/session/submit-chunk", response_model=InterviewChunkSubmitResponse)
def submit_chunk(
    video: UploadFile = File(...),
    session_token: str = Form(...),
    prompt_id: str = Form(...),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    session = db.query(InterviewSession).filter_by(session_token=session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    os.makedirs("uploads", exist_ok=True)
    video_path = f"uploads/{session_token}_{prompt_id}.webm"
    with open(video_path, "wb") as f:
        f.write(video.file.read())

    candidate = db.query(Candidate).filter_by(id=session.candidate_id).first()
    transcript = transcribe(language, video_path)
    current = session.transcript or ""
    session.transcript = f"{current}\n{transcript}".strip()
    db.add(session)
    db.commit()
    role_applied = candidate.role_applied if candidate else "electrician"
    questions = get_questions(role_applied, language, db=db)
    current_question = next((question for question in questions if question["id"] == prompt_id), None)
    question_index = next(
        (index for index, question in enumerate(questions) if question["id"] == prompt_id),
        None,
    )
    next_question = None
    if question_index is not None and question_index + 1 < len(questions):
        next_question = questions[question_index + 1]["text"]

    if current_question:
        db.add(
            QuestionResponse(
                session_id=session.id,
                question_key=current_question["id"],
                question_text=current_question["text"],
                transcript=transcript,
                order_index=current_question["order_index"],
            )
        )
        db.commit()

    return InterviewChunkSubmitResponse(
        prompt_id=prompt_id,
        transcript=transcript,
        status=session.status,
        next_question=next_question,
    )


@router.post("/session/finalize", response_model=InterviewFinalizeResponse)
def finalize_session(
    payload: InterviewFinalizeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    session = db.query(InterviewSession).filter_by(session_token=payload.session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    candidate = db.query(Candidate).filter_by(id=session.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    if session.status == "COMPLETED":
        return InterviewFinalizeResponse(
            candidate_id=candidate.id,
            session_id=session.id,
            status=session.status,
            message="Interview session has already been finalized.",
        )

    session.status = "PROCESSING"
    session.completed = False
    db.add(session)
    db.commit()
    background_tasks.add_task(run_interview_pipeline, session.id, payload.role_applied, payload.language)

    return InterviewFinalizeResponse(
        candidate_id=candidate.id,
        session_id=session.id,
        status=session.status,
        message="Interview finalization has started.",
    )


@router.get("/session/{session_id}/status", response_model=InterviewStatusResponse)
def get_session_status(session_id: int, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    candidate = db.query(Candidate).filter_by(id=session.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    return InterviewStatusResponse(
        candidate_id=candidate.id,
        session_id=session.id,
        status=session.status,
        fitment_label=candidate.fitment_label,
        overall_score=candidate.overall_score,
        confidence_score=candidate.confidence_score,
        next_step_message=(
            "You are ready for the next hiring stage."
            if candidate.fitment_label == "JOB_READY"
            else "Your profile will be reviewed by an officer."
            if session.status == "COMPLETED"
            else None
        ),
    )


@router.get("/questions/{role}/{language}", response_model=InterviewQuestionSetResponse)
def fetch_questions(role: str, language: str, db: Session = Depends(get_db)):
    questions = [InterviewQuestion(**item) for item in get_questions(role, language, db=db)]
    return InterviewQuestionSetResponse(role=role, language=language, questions=questions)

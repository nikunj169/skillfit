from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.dependencies import get_db
from backend.middleware.auth import verify_admin_token
from backend.models.assessment import Assessment
from backend.models.candidate import Candidate
from backend.models.question_response import QuestionResponse
from backend.models.session import InterviewSession
from backend.schemas.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminStatsResponse,
    CandidateDetail,
    CandidateListResponse,
    CandidateSummary,
    ShortlistRequest,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest):
    settings = get_settings()
    if payload.username != "admin@skillfit.in" or payload.password != "skillfit2024":
        raise HTTPException(status_code=401, detail="Invalid admin credentials.")
    return AdminLoginResponse(token=settings.admin_token, message="Login successful.")


@router.get("/candidates", response_model=CandidateListResponse)
def list_candidates(db: Session = Depends(get_db), _: str = Depends(verify_admin_token)):
    candidates = db.query(Candidate).order_by(Candidate.created_at.desc()).all()
    items = [
        CandidateSummary(
            id=item.id,
            full_name=item.full_name,
            district=item.district,
            role_applied=item.role_applied,
            language=item.language,
            status=item.status,
            workforce_category=item.workforce_category,
            fitment_label=item.fitment_label,
            overall_score=item.overall_score,
            confidence_score=item.confidence_score,
            shortlisted=item.shortlisted,
        )
        for item in candidates
    ]
    return CandidateListResponse(items=items, total=len(items))


@router.get("/candidates/{candidate_id}", response_model=CandidateDetail)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin_token),
):
    candidate = db.query(Candidate).filter_by(id=candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    latest_session = (
        db.query(InterviewSession)
        .filter_by(candidate_id=candidate.id)
        .order_by(InterviewSession.created_at.desc(), InterviewSession.id.desc())
        .first()
    )
    latest_assessment = (
        db.query(Assessment)
        .filter_by(candidate_id=candidate.id)
        .order_by(Assessment.created_at.desc(), Assessment.id.desc())
        .first()
    )
    response_history = []
    if latest_session:
        response_history = (
            db.query(QuestionResponse)
            .filter_by(session_id=latest_session.id)
            .order_by(QuestionResponse.order_index.asc(), QuestionResponse.id.asc())
            .all()
        )

    return CandidateDetail(
        id=candidate.id,
        full_name=candidate.full_name,
        district=candidate.district,
        role_applied=candidate.role_applied,
        language=candidate.language,
        status=candidate.status,
        workforce_category=candidate.workforce_category,
        fitment_label=candidate.fitment_label,
        overall_score=candidate.overall_score,
        confidence_score=candidate.confidence_score,
        shortlisted=candidate.shortlisted,
        phone_number=candidate.phone_number,
        integrity_flags=candidate.integrity_flags or [],
        face_presence_ratio=candidate.face_presence_ratio,
        latest_transcript=latest_session.transcript if latest_session else "",
        latest_session_status=latest_session.status if latest_session else "PENDING",
        latest_assessment=(
            {
                "clarity_score": latest_assessment.clarity_score,
                "confidence_score": latest_assessment.confidence_score,
                "relevance_score": latest_assessment.relevance_score,
                "overall_score": latest_assessment.overall_score,
                "strengths": latest_assessment.strengths,
                "improvement_areas": latest_assessment.improvement_areas,
            }
            if latest_assessment
            else None
        ),
        response_history=[
            {
                "question_key": response.question_key,
                "question_text": response.question_text,
                "transcript": response.transcript,
                "order_index": response.order_index,
                "relevance_score": response.relevance_score,
                "completeness_score": response.completeness_score,
                "clarity_score": response.clarity_score,
                "skill_confidence_score": response.skill_confidence_score,
                "llm_notes": response.llm_notes,
            }
            for response in response_history
        ],
    )


@router.patch("/candidates/{candidate_id}/status", response_model=CandidateDetail)
def shortlist_candidate(
    candidate_id: int,
    payload: ShortlistRequest,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin_token),
):
    candidate = db.query(Candidate).filter_by(id=candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    candidate.shortlisted = payload.shortlisted
    candidate.status = "shortlisted" if payload.shortlisted else "manual_review"
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return CandidateDetail(
        id=candidate.id,
        full_name=candidate.full_name,
        district=candidate.district,
        role_applied=candidate.role_applied,
        language=candidate.language,
        status=candidate.status,
        workforce_category=candidate.workforce_category,
        fitment_label=candidate.fitment_label,
        overall_score=candidate.overall_score,
        confidence_score=candidate.confidence_score,
        shortlisted=candidate.shortlisted,
        phone_number=candidate.phone_number,
        integrity_flags=candidate.integrity_flags or [],
        face_presence_ratio=candidate.face_presence_ratio,
        latest_transcript="",
        latest_session_status="PENDING",
        latest_assessment=None,
        response_history=[],
    )


@router.get("/stats", response_model=AdminStatsResponse)
def get_stats(db: Session = Depends(get_db), _: str = Depends(verify_admin_token)):
    candidates = db.query(Candidate).all()
    return AdminStatsResponse(
        total_candidates=len(candidates),
        shortlisted_candidates=sum(1 for candidate in candidates if candidate.shortlisted),
        pending_review=sum(1 for candidate in candidates if candidate.status in {"pending", "manual_review"}),
        job_ready=sum(1 for candidate in candidates if candidate.fitment_label == "JOB_READY"),
    )

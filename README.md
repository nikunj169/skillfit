# SkillFit — AI-Powered Multilingual Video Assessment Platform

> **AI SkillFit** is a mobile-first, multilingual video interview and workforce fitment platform built for Karnataka's Directorate of Electronic Delivery of Citizen Services (EDCS). It enables scalable, AI-led screening of blue-collar and polytechnic-skilled candidates in Kannada, Hindi, and English — with no app installation required.

---

## Table of Contents

- [Problem Context](#problem-context)
- [Solution Overview](#solution-overview)
- [Current Implementation Status](#current-implementation-status)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Core Modules](#core-modules)
- [Data Flow & Implementation Workflow](#data-flow--implementation-workflow)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)
- [Demo Flow (Round 2)](#demo-flow-round-2)
- [Evaluation Criteria Mapping](#evaluation-criteria-mapping)
- [Technology Decisions & Rationale](#technology-decisions--rationale)
- [Known Limitations & Future Work](#known-limitations--future-work)

---

## Current Implementation Status

The repository now includes a working starter implementation for both the frontend and backend.

### Completed So Far

- Vite + React frontend bootstrapped with root scripts and local build support
- FastAPI backend bootstrapped with SQLite-friendly local defaults
- Candidate interview flow scaffolded in the frontend:
  landing, registration, permission gate, interview, processing, and result pages
- Admin flow scaffolded in the frontend:
  login, dashboard, stats, candidate list, and candidate detail view
- Admin candidate detail now includes the latest stored transcript and latest assessment breakdown when available
- Per-question candidate responses are now persisted and shown in the admin detail view
- Backend endpoints implemented for:
  session start, question fetch, chunk submit, session finalize, session status, admin login, candidate list, candidate detail, candidate status update, and admin stats
- Interview finalization now uses a lightweight background-processing step:
  the finalize endpoint marks the session as `PROCESSING`, the backend completes assessment/classification in a background task, and the status endpoint exposes the final result
- Question bank persistence has been partially implemented:
  a `questions` table model exists, the API can read seeded DB questions, and `scripts/seed_questions.py` now seeds starter role/language question sets
- Docker Compose, Nginx, and Kubernetes starter infrastructure files added
- Basic backend tests passing for core API flow

### Current Scope of the Prototype

- The interview flow now submits actual video blobs via the `MediaRecorder` API
- ASR is a starter placeholder or API-key gated
- Text-to-Speech (TTS) for question delivery is now fully functional using the browser-native `window.speechSynthesis` API
- Face Validation is now powered by real MediaPipe/OpenCV ML logic, processing uploaded video blobs at 2fps to verify candidate presence
- LLM Assessment Engine is now integrated with the OpenAI API using structured JSON output to score transcripts automatically
- Duplicate detection now uses SQLite-compatible cosine similarity over stored embeddings (DeepFace face-embedding extraction planned for production)
- Audio Validation now computes real SNR and silence ratio when `ffmpeg` is available; gracefully falls back to mock values when it is not
- Admin detail now includes a full per-question audit trail with per-question scoring and AI notes
- Admin action buttons are now functional, allowing recruiters to officially shortlist candidates from the detail view
- Question lookup still keeps a code fallback so local development works even before seeding
- The processing screen now uses the session-status endpoint, and interview finalization now runs through a lightweight backend background task
- SQLite is sufficient for local development; PostgreSQL/pgvector remains the next infrastructure upgrade for production parity

---

## Problem Context

Karnataka has hundreds of thousands of blue-collar and polytechnic-skilled candidates distributed across districts who require screening for government job placements and training programs. The current process is:

- **Fragmented**: No standardized assessment pipeline across districts
- **Language-exclusive**: Text-heavy digital forms exclude Kannada-speaking candidates with low digital literacy
- **Unscalable**: Manual interviews cannot handle high-volume intake
- **Integrity-weak**: No mechanism to detect duplicate submissions, impersonation, or low-quality inputs
- **Inconsistent**: Assessment quality varies heavily by interviewer and region

Most candidates are mobile-comfortable and voice-first — yet no existing system meets them where they are.

---

## Solution Overview

SkillFit conducts structured AI-led video interviews on a mobile browser (zero app install), assesses candidate responses, validates session integrity, detects duplicates via face embeddings, and classifies candidates into actionable fitment tiers. Government officers access a dashboard to shortlist, review, and route candidates.

### Fitment Classifications

| Label | Meaning |
|---|---|
| `JOB_READY` | Strong responses, high confidence, clean integrity |
| `REQUIRES_UPSKILLING` | Competent but gaps detected; route to training |
| `REQUIRES_MANUAL_VERIFICATION` | Ambiguous signals; human review needed |
| `LOW_QUALITY_SUBMISSION` | Poor audio/video or incoherent responses |
| `SUSPECTED_DUPLICATE` | Face embedding similarity above threshold |

### Workforce Category Mapping

| Category | Examples |
|---|---|
| `BLUE_COLLAR_TRADE` | Plumber, electrician, welder, mason |
| `POLYTECHNIC_SKILLED` | Diploma-holder, ITI graduate, lab technician |
| `SEMI_SKILLED` | Delivery, packing, retail, assembly |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CANDIDATE (Mobile Browser)               │
│              React PWA — No App Install Required                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS (REST + WebSocket)
┌──────────────────────────▼──────────────────────────────────────┐
│                     FastAPI Backend (Python)                     │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  Interview  │  │  Assessment  │  │  Integrity & Duplicate │  │
│  │   Agent     │  │   Engine     │  │  Detection Layer       │  │
│  └──────┬──────┘  └──────┬───────┘  └───────────┬───────────┘  │
│         │                │                       │              │
│  ┌──────▼──────┐  ┌──────▼───────┐  ┌───────────▼───────────┐  │
│  │  Sarvam AI  │  │  Claude /    │  │  MediaPipe (presence)  │  │
│  │  Saarika    │  │  GPT-4o LLM  │  │  DeepFace (embedding)  │  │
│  │  (KN/HI)   │  │  (Scoring)   │  │  PostgreSQL (vectors)  │  │
│  │  Whisper   │  └──────────────┘  └───────────────────────┘  │
│  │  (EN ASR)  │                                                 │
│  └────────────┘                                                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Classification & Fitment Engine              │   │
│  │         (Rule-based + LLM score aggregation)              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     PostgreSQL + pgvector                 │   │
│  │         Candidate records, transcripts, embeddings        │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  Admin Dashboard (React)                         │
│   Filter / Shortlist / Review / Flag — Government Stakeholders  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
skillfit/
│
├── README.md
├── docker-compose.yml
├── .env.example
│
├── frontend/                          # React PWA (Candidate + Admin)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── routes/
│   │   │   ├── CandidateRoutes.jsx
│   │   │   └── AdminRoutes.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── candidate/
│   │   │   │   ├── Landing.jsx            # Language selector + entry point
│   │   │   │   ├── Registration.jsx       # Name, district, role applied for
│   │   │   │   ├── Interview.jsx          # Core interview UI (camera + AI voice)
│   │   │   │   ├── InterviewComplete.jsx  # Classification result shown to candidate
│   │   │   │   └── PermissionGate.jsx     # Camera/mic permission prompt
│   │   │   │
│   │   │   └── admin/
│   │   │       ├── Dashboard.jsx          # Main officer view
│   │   │       ├── CandidateDetail.jsx    # Full record with transcript + scores
│   │   │       ├── Filters.jsx            # District / skill / language / status
│   │   │       └── Login.jsx              # Admin auth
│   │   │
│   │   ├── components/
│   │   │   ├── VideoRecorder.jsx          # MediaRecorder API wrapper
│   │   │   ├── AIVoicePrompt.jsx          # Text-to-speech question delivery
│   │   │   ├── ProgressStepper.jsx        # Interview step indicator
│   │   │   ├── FitmentBadge.jsx           # Classification label display
│   │   │   ├── ScoreCard.jsx              # Per-dimension score breakdown
│   │   │   ├── IntegrityFlag.jsx          # Red/yellow flag indicator
│   │   │   └── LanguageToggle.jsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useMediaRecorder.js
│   │   │   ├── useInterviewSession.js
│   │   │   └── useAdminFilters.js
│   │   │
│   │   ├── context/
│   │   │   ├── SessionContext.jsx         # Candidate session state
│   │   │   └── AdminContext.jsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.js                     # Axios instance + interceptors
│   │   │   ├── interview.service.js
│   │   │   └── admin.service.js
│   │   │
│   │   ├── i18n/
│   │   │   ├── index.js                   # i18next config
│   │   │   ├── en.json
│   │   │   ├── kn.json                    # Kannada UI strings
│   │   │   └── hi.json
│   │   │
│   │   └── utils/
│   │       ├── audioHelpers.js
│   │       └── formatters.js
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/                           # FastAPI Python backend
│   ├── main.py                        # App entry point, router registration
│   ├── config.py                      # Settings via pydantic-settings
│   ├── dependencies.py                # DB session, auth dependencies
│   │
│   ├── routers/
│   │   ├── interview.py               # POST /session/start, /session/submit-chunk
│   │   ├── assessment.py              # POST /assess
│   │   ├── integrity.py               # POST /validate-face, /check-duplicate
│   │   ├── classification.py          # POST /classify
│   │   └── admin.py                   # GET /candidates, /candidate/:id, PATCH /shortlist
│   │
│   ├── services/
│   │   ├── asr/
│   │   │   ├── sarvam_client.py       # Sarvam AI Saarika ASR (Kannada + Hindi)
│   │   │   ├── whisper_client.py      # OpenAI Whisper ASR (English)
│   │   │   └── asr_router.py          # Language → correct ASR client
│   │   │
│   │   ├── assessment/
│   │   │   ├── llm_assessor.py        # LLM call with structured JSON output
│   │   │   ├── prompt_templates.py    # Per-role, per-language prompt templates
│   │   │   └── score_aggregator.py    # Aggregate per-question scores → overall
│   │   │
│   │   ├── integrity/
│   │   │   ├── face_validator.py      # MediaPipe face detection per frame
│   │   │   ├── audio_validator.py     # SNR / silence ratio checks
│   │   │   └── duplicate_detector.py  # DeepFace embedding + cosine similarity
│   │   │
│   │   ├── classification/
│   │   │   └── fitment_classifier.py  # Rule engine over aggregated scores + flags
│   │   │
│   │   └── tts/
│   │       └── tts_client.py          # Text-to-speech for question delivery (Sarvam / gTTS)
│   │
│   ├── models/
│   │   ├── candidate.py               # SQLAlchemy ORM model
│   │   ├── session.py
│   │   ├── assessment.py
│   │   └── embedding.py               # Face vector store model
│   │
│   ├── schemas/
│   │   ├── interview.py               # Pydantic request/response schemas
│   │   ├── assessment.py
│   │   ├── classification.py
│   │   └── admin.py
│   │
│   ├── db/
│   │   ├── base.py                    # SQLAlchemy declarative base
│   │   ├── session.py                 # Engine + SessionLocal factory
│   │   └── migrations/                # Alembic migration scripts
│   │       └── versions/
│   │
│   ├── tasks/
│   │   └── async_pipeline.py          # Background task: ASR → assess → classify
│   │
│   ├── middleware/
│   │   └── auth.py                    # JWT middleware for admin routes
│   │
│   ├── tests/
│   │   ├── test_asr.py
│   │   ├── test_assessment.py
│   │   ├── test_integrity.py
│   │   ├── test_classification.py
│   │   └── conftest.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── scripts/
│   ├── seed_questions.py              # Seed interview question bank to DB
│   ├── seed_admin.py                  # Create default admin user
│   └── test_sarvam.py                 # Standalone Sarvam ASR smoke test
│
└── infra/
    ├── docker-compose.yml
    ├── nginx.conf                     # Reverse proxy config
    └── k8s/                           # Optional Kubernetes manifests
        ├── deployment.yaml
        ├── service.yaml
        └── configmap.yaml
```

---

## Core Modules

### 1. Interview Agent (`routers/interview.py` + `services/tts/`)

The candidate opens the web app and selects a language. The backend delivers structured questions via text-to-speech (Sarvam AI TTS for Kannada/Hindi, browser Web Speech API or gTTS for English). Each question response is captured as a video chunk via the browser's `MediaRecorder` API and uploaded as a binary blob.

**Sequence:**
1. `POST /session/start` — creates a session record, returns `session_id` + first question audio
2. `POST /session/submit-chunk` — receives video blob for each question, queues async processing
3. `POST /session/finalize` — triggers full pipeline after all chunks received

### 2. ASR Transcription (`services/asr/`)

Language-routed transcription:

| Language | Model | Reason |
|---|---|---|
| Kannada | Sarvam AI Saarika v1 | Purpose-built Indic ASR, dialectal robustness |
| Hindi | Sarvam AI Saarika v1 | Same model, same robustness benefits |
| English | OpenAI Whisper (large-v3) | High accuracy for standard English |

`asr_router.py` reads the session language field and delegates to the correct client. Both clients return a normalized `TranscriptionResult(text, confidence, language_detected)` object consumed downstream.

### 3. Response Assessment Engine (`services/assessment/`)

The LLM (Claude claude-sonnet-4-20250514 or GPT-4o) receives the transcribed candidate response alongside the original question and role context. It returns a structured JSON object:

```json
{
  "relevance_score": 0.82,
  "completeness_score": 0.74,
  "clarity_score": 0.68,
  "skill_confidence_score": 0.71,
  "flag": null,
  "notes": "Candidate demonstrated practical knowledge but response was partially unclear due to heavy dialect."
}
```

Prompts are templatized per role (e.g., electrician vs. delivery associate) and per language to avoid penalizing natural informal speech patterns in Kannada. The `score_aggregator.py` combines per-question scores into weighted session-level scores.

### 4. Face & Audio Integrity Validation (`services/integrity/`)

**Face Validation (`face_validator.py`):**
- Extracts frames from the uploaded video at 2 fps using OpenCV
- Runs MediaPipe Face Detection on each frame
- Computes `face_presence_ratio = frames_with_face / total_frames`
- Sessions with `face_presence_ratio < 0.6` are flagged as `LOW_QUALITY`

**Audio Validation (`audio_validator.py`):**
- Extracts audio track using `ffmpeg-python`
- Computes Signal-to-Noise Ratio (SNR) and silence fraction
- Sessions with `SNR < 10dB` or `silence_ratio > 0.5` are flagged

**Duplicate Detection (`duplicate_detector.py`):**
- Uses DeepFace to extract a 512-dim face embedding from a clean frame
- Stores embedding in PostgreSQL via `pgvector`
- On each new submission, computes cosine similarity against all stored embeddings for the same intake batch
- Similarity `> 0.85` → `SUSPECTED_DUPLICATE` flag

### 5. Fitment Classification (`services/classification/fitment_classifier.py`)

Rule engine operating over aggregated scores + integrity flags:

```
if SUSPECTED_DUPLICATE flag → SUSPECTED_DUPLICATE (override all)
elif LOW_QUALITY flag OR face_presence_ratio < 0.6 → LOW_QUALITY_SUBMISSION
elif REQUIRES_MANUAL_VERIFICATION flag → REQUIRES_MANUAL_VERIFICATION
elif overall_score >= 0.75 AND no flags → JOB_READY
elif overall_score >= 0.45 → REQUIRES_UPSKILLING
else → REQUIRES_MANUAL_VERIFICATION
```

Workforce category is determined by the candidate's self-declared role mapped against a lookup table of roles → categories.

### 6. Admin Dashboard (`routers/admin.py` + `frontend/pages/admin/`)

REST endpoints power a React dashboard with:

- **Filter panel**: district, skill category, language, fitment label, date range
- **Candidate list**: paginated table with sortable columns
- **Detail view**: full transcript per question, per-dimension scores, face presence ratio, duplicate flag status, integrity summary
- **Action buttons**: Shortlist for Job / Shortlist for Training / Flag for Manual Review / Reject

---

## Data Flow & Implementation Workflow

```
Candidate opens mobile browser
           │
           ▼
  Language selection (KN / HI / EN)
  + Basic registration (name, district, role)
           │
           ▼
  Session created in DB
  Questions fetched for role
  TTS audio generated and sent
           │
           ▼
  ┌─────── Interview Loop (per question) ────────────┐
  │                                                   │
  │  AI voice delivers question                       │
  │  Candidate records video response (30–90 sec)     │
  │  Video chunk uploaded to backend                  │
  │                                                   │
  │  Async pipeline triggered per chunk:              │
  │    1. Extract audio from video (ffmpeg)           │
  │    2. ASR transcription (Sarvam / Whisper)        │
  │    3. Store transcript in DB                      │
  │    4. LLM assessment → scores stored              │
  │    5. Face frame extraction (OpenCV)              │
  │    6. Face presence check (MediaPipe)             │
  │    7. Audio quality check (SNR)                   │
  │                                                   │
  └────────── Repeat for all N questions ─────────────┘
           │
           ▼
  Session finalized
  Duplicate detection runs (DeepFace + pgvector)
  Scores aggregated across all questions
  Fitment classification computed
  Candidate record updated with final label
           │
           ▼
  Result shown to candidate (simple label + next steps)
           │
           ▼
  Admin dashboard updated in real-time
  Officer reviews → actions candidate
```

---

## API Reference

### Candidate-Facing Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/session/start` | Create session, receive first question |
| `POST` | `/api/v1/session/submit-chunk` | Upload video blob for one question |
| `POST` | `/api/v1/session/finalize` | Finalize session, trigger classification |
| `GET` | `/api/v1/session/{session_id}/status` | Poll for classification result |
| `GET` | `/api/v1/questions/{role}/{language}` | Fetch question set |

### Admin Endpoints (JWT Protected)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/admin/login` | Admin authentication |
| `GET` | `/api/v1/admin/candidates` | List candidates with filters |
| `GET` | `/api/v1/admin/candidates/{id}` | Full candidate record |
| `PATCH` | `/api/v1/admin/candidates/{id}/status` | Update status (shortlist/reject/flag) |
| `GET` | `/api/v1/admin/stats` | Aggregated dashboard stats |

---

## Database Schema

### `candidates`

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key |
| `name` | TEXT | |
| `district` | TEXT | |
| `role_applied` | TEXT | |
| `language` | ENUM(kn, hi, en) | |
| `fitment_label` | ENUM | See classification labels |
| `workforce_category` | ENUM | |
| `overall_score` | FLOAT | 0–1 |
| `integrity_flags` | JSONB | List of active flags |
| `face_presence_ratio` | FLOAT | |
| `status` | ENUM | shortlisted/rejected/pending/manual_review |
| `created_at` | TIMESTAMP | |

### `sessions`

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | |
| `candidate_id` | UUID | FK → candidates |
| `completed` | BOOL | |
| `finalized_at` | TIMESTAMP | |

### `question_responses`

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | |
| `session_id` | UUID | FK → sessions |
| `question_id` | UUID | FK → questions |
| `transcript` | TEXT | ASR output |
| `relevance_score` | FLOAT | |
| `completeness_score` | FLOAT | |
| `clarity_score` | FLOAT | |
| `skill_confidence_score` | FLOAT | |
| `asr_confidence` | FLOAT | |
| `llm_notes` | TEXT | |

Current implementation note:
- The prototype now persists per-question response text in a `question_responses` table with question key/text, transcript, and order index.
- Per-question scoring fields from the target design are not stored yet; assessment remains session-level for now.

### `face_embeddings`

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | |
| `candidate_id` | UUID | FK → candidates |
| `embedding` | VECTOR(512) | pgvector column |
| `created_at` | TIMESTAMP | |

### `questions`

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | |
| `role` | TEXT | e.g., `electrician`, `delivery_associate` |
| `language` | ENUM | |
| `question_text` | TEXT | |
| `question_audio_url` | TEXT | Pre-generated TTS |
| `order_index` | INT | |

Current implementation note:
- The prototype now includes a SQLAlchemy `questions` model and a working seed script for starter interview questions.
- The question API reads from the database when rows are present and falls back to the in-code bank otherwise.
- The candidate frontend now includes a processing/status route before the final result screen to match the documented interview flow more closely.

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15+ with `pgvector` extension
- `ffmpeg` installed on host or container

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run Alembic migrations
alembic upgrade head

# Seed question bank
python ../scripts/seed_questions.py

# Create default admin user
python ../scripts/seed_admin.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev       # Development server on http://localhost:5173
```

---

## Environment Variables

Create a `.env` file in `backend/` based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://skillfit:skillfit@localhost:5432/skillfit_db

# Sarvam AI
SARVAM_API_KEY=your_sarvam_api_key
SARVAM_ASR_ENDPOINT=https://api.sarvam.ai/speech-to-text

# OpenAI (Whisper + optional GPT-4o)
OPENAI_API_KEY=your_openai_api_key

# Anthropic (Claude assessment)
ANTHROPIC_API_KEY=your_anthropic_api_key

# LLM Provider: "claude" or "openai"
LLM_PROVIDER=claude

# JWT
JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=480

# Face Embedding
DUPLICATE_SIMILARITY_THRESHOLD=0.85
FACE_PRESENCE_MIN_RATIO=0.6

# Storage (local or S3)
STORAGE_BACKEND=local           # or "s3"
LOCAL_STORAGE_PATH=./uploads
AWS_BUCKET_NAME=skillfit-videos
AWS_REGION=ap-south-1
```

---

## Running Locally

```bash
# Terminal 1 — Start PostgreSQL
docker run -d \
  --name skillfit-db \
  -e POSTGRES_USER=skillfit \
  -e POSTGRES_PASSWORD=skillfit \
  -e POSTGRES_DB=skillfit_db \
  -p 5432:5432 \
  ankane/pgvector

# Terminal 2 — Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 — Frontend
cd frontend
npm run dev
```

Access:
- Candidate interface: `http://localhost:5173/`
- Admin dashboard: `http://localhost:5173/admin`
- API docs (Swagger): `http://localhost:8000/docs`

Small next-step note:
- If you want the documented question-bank workflow, run `python scripts/seed_questions.py` from the repo root after starting the backend environment once.

---

## Running with Docker

```bash
# Build and start all services
docker compose up --build

# Run migrations inside container
docker compose exec backend alembic upgrade head

# Seed data
docker compose exec backend python ../scripts/seed_questions.py
docker compose exec backend python ../scripts/seed_admin.py
```

Default admin credentials (dev only): `admin@skillfit.in` / `skillfit2024`

### `docker-compose.yml` Overview

```yaml
services:
  db:
    image: ankane/pgvector
    environment:
      POSTGRES_USER: skillfit
      POSTGRES_PASSWORD: skillfit
      POSTGRES_DB: skillfit_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_BASE_URL=http://localhost:8000

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./infra/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
```

---

## Demo Flow (Round 2)

The Round 2 prototype demonstrates an end-to-end flow:

1. **Candidate opens mobile browser** → selects Kannada
2. **Enters name, district (e.g., Dharwad), role (Electrician)**
3. **Interview begins**: AI voice asks 3 structured questions in Kannada
4. **Candidate responds** by speaking into phone camera
5. **Processing screen** shows while ASR → LLM pipeline runs
6. **Result screen**: Candidate sees their fitment label and next step message in Kannada

Current prototype note:
- The UI now includes the processing screen and checks the session-status endpoint before showing results.
- The backend now performs a lightweight background finalization step, though it is still not a full external queue/worker architecture yet.
7. **Admin dashboard**: Officer filters by Dharwad district, sees new candidate with transcript, per-dimension scores, and integrity status — clicks Shortlist for Training

---

## Evaluation Criteria Mapping

| Criterion | Implementation |
|---|---|
| Kannada + multilingual quality | Sarvam Saarika ASR (Kannada/Hindi), Whisper (English), i18n UI |
| Dialectal robustness | Saarika trained on dialectal Indic speech; LLM prompted to not penalize informal phrasing |
| Assessment accuracy | LLM scoring with 4 dimensions; per-role prompt templates |
| Integrity detection | MediaPipe face presence + audio SNR + DeepFace duplicate detection |
| Fitment classification | Rule engine with 5 classification tiers + 3 workforce categories |
| Dashboard usability | Filter by district/language/status; transcript + scores per candidate; one-click actions |
| Scalability | Stateless async pipeline; horizontal scale at interview layer; containerized |
| Deployment readiness | Docker Compose for local; K8s manifests for production |

---

## Technology Decisions & Rationale

**Sarvam AI Saarika over Whisper for Kannada:**
Whisper's Kannada support is limited and fails badly on informal dialectal speech. Saarika is built specifically for Indian languages with training data that includes regional dialects. This is the strongest available ASR for this use case in India as of 2024.

**DeepFace over a custom embedding model:**
DeepFace provides production-grade face embeddings (ArcFace/Facenet backends) with zero training overhead. Combined with pgvector for fast cosine similarity search, it meets the duplicate detection requirement without custom model development.

**MediaPipe for presence detection (not recognition):**
We deliberately separate face presence validation (MediaPipe — fast, lightweight, runs on extracted frames) from identity verification (DeepFace — heavier, used only for duplicate comparison). This separation keeps the per-frame validation cheap.

**Rule-based classification over end-to-end ML:**
An end-to-end ML classifier would require labeled training data we do not have. A rule engine over interpretable LLM-generated scores is auditable, tuneable by domain experts, and does not require dataset collection to function correctly.

**React PWA over native app:**
Zero install friction is a hard requirement for low-digital-literacy candidates. A mobile-responsive web app that uses `MediaRecorder` API provides all necessary capabilities without app store friction.

---

## Known Limitations & Future Work

- **LLM latency**: Processing each response takes 5–15 seconds. Current mitigation is async queuing with a progress screen. Caching question-level results per session minimizes re-processing.
- **Offline support**: The current implementation requires a stable internet connection. Edge-caching of questions and offline recording with deferred upload is a planned extension.
- **TTS quality in Kannada**: Browser Web Speech API Kannada support is inconsistent. Sarvam TTS API is the preferred fallback but adds latency on first load; we pre-generate audio for the question bank.
- **Face embedding cold storage**: Large-scale deployments (100K+ candidates) will require ANN indexing (e.g., HNSW via pgvector) rather than linear scan for duplicate detection — this is already supported by pgvector and needs only index creation.
- **Role coverage**: The current question bank covers Electrician, Plumber, Delivery Associate, and Retail Staff. Expanding to 50+ roles requires a question authoring workflow for domain experts.

---

## License

This project was developed for the AI SkillFit hackathon problem statement issued by the Directorate of Electronic Delivery of Citizen Services (EDCS), Karnataka. All third-party models and APIs are subject to their respective licenses and terms of service.



run backend:- .venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

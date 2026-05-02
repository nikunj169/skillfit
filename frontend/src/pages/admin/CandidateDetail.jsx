import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import FitmentBadge from "../../components/FitmentBadge";
import IntegrityFlag from "../../components/IntegrityFlag";
import { getCandidateDetail } from "../../services/admin.service";
import { formatScore } from "../../utils/formatters";

function CandidateDetail() {
  const { candidateId } = useParams();
  const [candidate, setCandidate] = useState(null);

  useEffect(() => {
    async function loadCandidate() {
      const response = await getCandidateDetail(candidateId);
      setCandidate(response);
    }

    loadCandidate();
  }, [candidateId]);

  if (!candidate) {
    return (
      <main className="screen">
        <section className="panel">
          <p>Loading candidate...</p>
        </section>
      </main>
    );
  }

  return (
    <main className="screen">
      <section className="panel">
        <Link className="text-link" to="/admin">
          Back to dashboard
        </Link>
        <p className="eyebrow">Candidate Detail</p>
        <h1>{candidate.full_name}</h1>
        <FitmentBadge label={candidate.fitment_label} />

        <div className="detail-grid">
          <div className="panel panel-soft">
            <h2>Profile</h2>
            <p>District: {candidate.district}</p>
            <p>Role: {candidate.role_applied}</p>
            <p>Language: {candidate.language}</p>
            <p>Workforce category: {candidate.workforce_category}</p>
            <p>Status: {candidate.status}</p>
            <p>Phone: {candidate.phone_number || "Not provided"}</p>
          </div>

          <div className="panel panel-soft">
            <h2>Assessment Summary</h2>
            <p>Overall score: {candidate.overall_score.toFixed(2)}</p>
            <p>Confidence score: {candidate.confidence_score.toFixed(2)}</p>
            <p>Latest session status: {candidate.latest_session_status}</p>
            <IntegrityFlag flags={candidate.integrity_flags || []} />
            {candidate.latest_assessment ? (
              <div className="stack-block">
                <p>Clarity: {formatScore(candidate.latest_assessment.clarity_score)}</p>
                <p>Assessment confidence: {formatScore(candidate.latest_assessment.confidence_score)}</p>
                <p>Relevance: {formatScore(candidate.latest_assessment.relevance_score)}</p>
                <p>Strengths: {(candidate.latest_assessment.strengths || []).join(", ") || "Not available"}</p>
                <p>
                  Improvement areas:{" "}
                  {(candidate.latest_assessment.improvement_areas || []).join(", ") || "Not available"}
                </p>
              </div>
            ) : (
              <p>No assessment record yet.</p>
            )}
          </div>

          <div className="panel panel-soft full-span">
            <h2>Latest Transcript</h2>
            <p className="transcript-block">
              {candidate.latest_transcript || "No transcript has been stored for this candidate yet."}
            </p>
          </div>

          <div className="panel panel-soft full-span">
            <h2>Per-Question Responses</h2>
            {candidate.response_history?.length ? (
              <div className="response-list">
                {candidate.response_history.map((response) => (
                  <article key={`${response.question_key}-${response.order_index}`} className="response-card">
                    <p className="section-kicker">Question {response.order_index}</p>
                    <h3>{response.question_text}</h3>
                    <p className="transcript-block">{response.transcript}</p>
                    {response.relevance_score !== null && response.relevance_score !== undefined && (
                      <div className="button-row" style={{ marginTop: "14px" }}>
                        <span className="chip">Relevance: {formatScore(response.relevance_score)}</span>
                        <span className="chip">Clarity: {formatScore(response.clarity_score)}</span>
                        <span className="chip">Completeness: {formatScore(response.completeness_score)}</span>
                        <span className="chip">Confidence: {formatScore(response.skill_confidence_score)}</span>
                      </div>
                    )}
                    {response.llm_notes && (
                      <p className="transcript-block" style={{ marginTop: "14px", color: "#a5c1ff" }}>
                        <strong>AI Notes:</strong> {response.llm_notes}
                      </p>
                    )}
                  </article>
                ))}
              </div>
            ) : (
              <p>No per-question responses have been stored yet.</p>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}

export default CandidateDetail;

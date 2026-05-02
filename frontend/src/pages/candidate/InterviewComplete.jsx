import { useNavigate } from "react-router-dom";
import FitmentBadge from "../../components/FitmentBadge";
import ScoreCard from "../../components/ScoreCard";
import { useSessionContext } from "../../context/SessionContext";

function InterviewComplete() {
  const navigate = useNavigate();
  const { result, resetSession } = useSessionContext();

  if (!result) {
    return (
      <main className="screen">
        <section className="panel">
          <h1>No completed interview found</h1>
          <button type="button" className="button button-primary" onClick={() => navigate("/")}>
            Go Home
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">Interview Complete</p>
        <h1>Candidate outcome</h1>
        <FitmentBadge label={result.fitment_label} />
        <p className="lede">{result.next_step_message}</p>

        <div className="metrics-grid">
          <ScoreCard title="Overall score" value={result.overall_score} description="Aggregated session score" />
          <ScoreCard title="Confidence" value={result.confidence_score} description="Classification confidence" />
        </div>

        <div className="button-row">
          <button
            type="button"
            className="button button-secondary"
            onClick={() => {
              resetSession();
              navigate("/");
            }}
          >
            Start Another Session
          </button>
          <button type="button" className="button button-primary" onClick={() => navigate("/admin/login")}>
            View Admin Side
          </button>
        </div>
      </section>
    </main>
  );
}

export default InterviewComplete;

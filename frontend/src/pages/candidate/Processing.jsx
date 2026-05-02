import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSessionContext } from "../../context/SessionContext";
import { useInterviewSession } from "../../hooks/useInterviewSession";
import { getInterviewStatus } from "../../services/interview.service";

function Processing() {
  const navigate = useNavigate();
  const { session, result, setResult } = useSessionContext();
  const { finishSession } = useInterviewSession();
  const [statusMessage, setStatusMessage] = useState("Submitting final interview answers...");
  const hasStartedRef = useRef(false);

  useEffect(() => {
    async function finalizeAndPoll() {
      if (!session) {
        navigate("/");
        return;
      }

      if (result) {
        navigate("/complete", { replace: true });
        return;
      }

      if (hasStartedRef.current) {
        return;
      }
      hasStartedRef.current = true;

      try {
        setStatusMessage("Finalizing interview session...");
        await finishSession();

        let latestStatus = await getInterviewStatus(session.session_id);
        while (latestStatus.status === "PROCESSING") {
          setStatusMessage("Checking classification status...");
          await new Promise((resolve) => window.setTimeout(resolve, 800));
          latestStatus = await getInterviewStatus(session.session_id);
        }

        if (latestStatus.status === "FAILED") {
          throw new Error("Interview processing failed.");
        }

        setResult({
          candidate_id: latestStatus.candidate_id,
          fitment_label: latestStatus.fitment_label,
          overall_score: latestStatus.overall_score,
          confidence_score: latestStatus.confidence_score,
          status: latestStatus.status,
          next_step_message: latestStatus.next_step_message || "Your interview review is complete.",
        });

        navigate("/complete", { replace: true });
      } catch {
        setStatusMessage("We could not complete processing. Please try the interview again.");
      }
    }

    finalizeAndPoll();
  }, [finishSession, navigate, result, session, setResult]);

  return (
    <main className="screen">
      <section className="panel panel-narrow">
        <p className="eyebrow">Processing</p>
        <h1>We are reviewing the interview now.</h1>
        <div className="loader-ring" aria-hidden="true" />
        <p className="lede">{statusMessage}</p>
        <p className="inline-status">This prototype uses the backend status endpoint before showing results.</p>
      </section>
    </main>
  );
}

export default Processing;

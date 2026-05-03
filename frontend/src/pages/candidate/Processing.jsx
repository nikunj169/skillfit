import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { useSessionContext } from "../../context/SessionContext";
import { useInterviewSession } from "../../hooks/useInterviewSession";
import { getInterviewStatus } from "../../services/interview.service";

function Processing() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { session, result, setResult } = useSessionContext();
  const { finishSession } = useInterviewSession();
  const [statusMessage, setStatusMessage] = useState(() => t("processing.statusSubmitting"));
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
        setStatusMessage(t("processing.statusFinalizing"));
        await finishSession();

        let latestStatus = await getInterviewStatus(session.session_id);
        while (latestStatus.status === "PROCESSING") {
          setStatusMessage(t("processing.statusChecking"));
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
          next_step_message: latestStatus.next_step_message || "",
        });

        navigate("/complete", { replace: true });
      } catch {
        setStatusMessage(t("processing.statusError"));
      }
    }

    finalizeAndPoll();
  }, [finishSession, navigate, result, session, setResult, t]);

  return (
    <main className="screen">
      <section className="panel panel-narrow">
        <p className="eyebrow">{t("processing.eyebrow")}</p>
        <h1>{t("processing.headline")}</h1>
        <div className="loader-ring" aria-hidden="true" />
        <p className="lede">{statusMessage}</p>
        <p className="inline-status">{t("processing.footerNote")}</p>
      </section>
    </main>
  );
}

export default Processing;

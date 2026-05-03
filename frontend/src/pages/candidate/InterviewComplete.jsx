import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import FitmentBadge from "../../components/FitmentBadge";
import ScoreCard from "../../components/ScoreCard";
import { useSessionContext } from "../../context/SessionContext";

function InterviewComplete() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { result, resetSession } = useSessionContext();

  if (!result) {
    return (
      <main className="screen">
        <section className="panel">
          <h1>{t("complete.noResult", "No completed interview found.")}</h1>
          <button type="button" className="button button-primary" onClick={() => navigate("/")}>
            {t("start", "Start")}
          </button>
        </section>
      </main>
    );
  }

  const localizedFitmentLabel = t(
    `complete.fitmentLabels.${result.fitment_label}`,
    { defaultValue: result.fitment_label }
  );
  const nextStepMessage = t(
    `complete.nextStepMessages.${result.fitment_label}`,
    { defaultValue: result.next_step_message || t("complete.nextStepMessages.REQUIRES_MANUAL_VERIFICATION") }
  );

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">{t("complete.eyebrow")}</p>
        <h1>{t("complete.headline")}</h1>
        <FitmentBadge label={result.fitment_label} displayLabel={localizedFitmentLabel} />
        <p className="lede">{nextStepMessage}</p>

        <div className="metrics-grid">
          <ScoreCard
            title={t("complete.scoreTitle")}
            value={result.overall_score}
            description={t("complete.scoreDesc")}
          />
          <ScoreCard
            title={t("complete.confidenceTitle")}
            value={result.confidence_score}
            description={t("complete.confidenceDesc")}
          />
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
            {t("complete.buttonNewSession")}
          </button>
          <button type="button" className="button button-primary" onClick={() => navigate("/admin/login")}>
            {t("complete.buttonAdminSide")}
          </button>
        </div>
      </section>
    </main>
  );
}

export default InterviewComplete;

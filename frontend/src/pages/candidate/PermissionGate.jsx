import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { useMediaRecorder } from "../../hooks/useMediaRecorder";

function PermissionGate() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { permissionState, requestPermissions } = useMediaRecorder();

  useEffect(() => {
    if (permissionState === "granted") {
      navigate("/interview");
    }
  }, [permissionState, navigate]);

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">{t("permissions.eyebrow")}</p>
        <h1>{t("permissions.headline")}</h1>
        <p className="lede">{t("permissions.body")}</p>

        {permissionState === "denied" && (
          <p className="error-text">{t("permissions.deniedError")}</p>
        )}

        <div className="button-row">
          <button type="button" className="button button-secondary" onClick={() => navigate("/register")}>
            {t("permissions.buttonBack")}
          </button>
          <button
            type="button"
            className="button button-primary"
            onClick={requestPermissions}
            disabled={permissionState === "granted"}
          >
            {permissionState === "denied" ? t("permissions.buttonTryAgain") : t("permissions.buttonAllow")}
          </button>
        </div>
      </section>
    </main>
  );
}

export default PermissionGate;

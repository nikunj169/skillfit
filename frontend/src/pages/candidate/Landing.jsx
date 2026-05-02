import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import LanguageToggle from "../../components/LanguageToggle";
import { useSessionContext } from "../../context/SessionContext";

function Landing() {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const { registration, setRegistration, resetSession } = useSessionContext();

  function handleLanguageChange(language) {
    setRegistration((current) => ({ ...current, language }));
    i18n.changeLanguage(language);
  }

  const liveItems = t("landing.liveItems", { returnObjects: true });

  return (
    <main className="screen">
      <section className="hero layout-split">
        <div>
          <p className="eyebrow">{t("landing.eyebrow")}</p>
          <h1>{t("landing.headline")}</h1>
          <p className="lede">{t("landing.lede")}</p>
          <LanguageToggle value={registration.language} onChange={handleLanguageChange} />
          <div className="button-row">
            <button
              type="button"
              className="button button-primary"
              onClick={() => {
                resetSession();
                navigate("/register");
              }}
            >
              {t("landing.startButton")}
            </button>
            <button type="button" className="button button-secondary" onClick={() => navigate("/admin/login")}>
              {t("landing.adminButton")}
            </button>
          </div>
        </div>

        <div className="panel panel-soft">
          <h2>{t("landing.liveTitle")}</h2>
          <ul className="clean-list">
            {Array.isArray(liveItems) && liveItems.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </section>
    </main>
  );
}

export default Landing;


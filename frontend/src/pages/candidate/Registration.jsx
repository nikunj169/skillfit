import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { useSessionContext } from "../../context/SessionContext";

const ROLES = ["Electrician", "Delivery Associate", "Plumber", "Welder"];

function Registration() {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const { registration, setRegistration } = useSessionContext();
  const [formState, setFormState] = useState(registration);

  function handleChange(field, value) {
    setFormState((current) => ({ ...current, [field]: value }));
  }

  function handleLanguageChange(value) {
    handleChange("language", value);
    i18n.changeLanguage(value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    setRegistration(formState);
    navigate("/permissions");
  }

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">{t("registration.eyebrow")}</p>
        <h1>{t("registration.headline")}</h1>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label className="form-field">
            <span>{t("registration.fullName")}</span>
            <input
              value={formState.full_name}
              onChange={(event) => handleChange("full_name", event.target.value)}
              required
            />
          </label>
          <label className="form-field">
            <span>{t("registration.district")}</span>
            <input
              value={formState.district}
              onChange={(event) => handleChange("district", event.target.value)}
              required
            />
          </label>
          <label className="form-field">
            <span>{t("registration.roleApplied")}</span>
            <select
              value={formState.role_applied}
              onChange={(event) => handleChange("role_applied", event.target.value)}
              required
            >
              {ROLES.map((role) => (
                <option key={role} value={role}>
                  {t(`registration.roles.${role}`, role)}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>{t("registration.interviewLanguage")}</span>
            <select
              value={formState.language}
              onChange={(event) => handleLanguageChange(event.target.value)}
              required
            >
              <option value="en">English (English)</option>
              <option value="hi">Hindi (हिंदी)</option>
              <option value="kn">Kannada (ಕನ್ನಡ)</option>
            </select>
          </label>
          <label className="form-field">
            <span>{t("registration.phoneNumber")}</span>
            <input
              value={formState.phone_number}
              onChange={(event) => handleChange("phone_number", event.target.value)}
            />
          </label>
          <div className="button-row">
            <button type="button" className="button button-secondary" onClick={() => navigate("/")}>
              {t("registration.buttonBack")}
            </button>
            <button type="submit" className="button button-primary">
              {t("registration.buttonContinue")}
            </button>
          </div>
        </form>
      </section>
    </main>
  );
}

export default Registration;

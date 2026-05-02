import { useNavigate } from "react-router-dom";
import LanguageToggle from "../../components/LanguageToggle";
import { useSessionContext } from "../../context/SessionContext";

function Landing() {
  const navigate = useNavigate();
  const { registration, setRegistration, resetSession } = useSessionContext();

  function handleLanguageChange(language) {
    setRegistration((current) => ({ ...current, language }));
  }

  return (
    <main className="screen">
      <section className="hero layout-split">
        <div>
          <p className="eyebrow">SkillFit Candidate Portal</p>
          <h1>Multilingual interview screening for mobile-first candidates.</h1>
          <p className="lede">
            Start in English, Hindi, or Kannada. The current prototype focuses on a guided transcript-based
            interview flow wired to the FastAPI backend.
          </p>
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
              Start Candidate Flow
            </button>
            <button type="button" className="button button-secondary" onClick={() => navigate("/admin/login")}>
              Open Admin Dashboard
            </button>
          </div>
        </div>

        <div className="panel panel-soft">
          <h2>What is live right now</h2>
          <ul className="clean-list">
            <li>Candidate registration</li>
            <li>Question fetching from backend</li>
            <li>Interview session creation and answer submission</li>
            <li>Result classification screen</li>
            <li>Admin login, stats, list, and detail view</li>
          </ul>
        </div>
      </section>
    </main>
  );
}

export default Landing;

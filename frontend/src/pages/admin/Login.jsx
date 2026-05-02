import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAdminContext } from "../../context/AdminContext";
import { loginAdmin } from "../../services/admin.service";

function Login() {
  const navigate = useNavigate();
  const { login } = useAdminContext();
  const [formState, setFormState] = useState({
    username: "admin@skillfit.in",
    password: "skillfit2024",
  });
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const response = await loginAdmin(formState);
      login(response.token);
      navigate("/admin");
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Unable to log in.");
    }
  }

  return (
    <main className="screen">
      <section className="panel panel-narrow">
        <p className="eyebrow">Admin Access</p>
        <h1>Sign in to SkillFit</h1>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label className="form-field">
            <span>Email</span>
            <input
              value={formState.username}
              onChange={(event) => setFormState((current) => ({ ...current, username: event.target.value }))}
            />
          </label>
          <label className="form-field">
            <span>Password</span>
            <input
              type="password"
              value={formState.password}
              onChange={(event) => setFormState((current) => ({ ...current, password: event.target.value }))}
            />
          </label>
          {error ? <p className="error-text">{error}</p> : null}
          <button type="submit" className="button button-primary">
            Sign In
          </button>
        </form>
      </section>
    </main>
  );
}

export default Login;

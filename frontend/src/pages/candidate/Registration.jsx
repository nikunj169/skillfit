import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSessionContext } from "../../context/SessionContext";

function Registration() {
  const navigate = useNavigate();
  const { registration, setRegistration } = useSessionContext();
  const [formState, setFormState] = useState(registration);

  function handleChange(field, value) {
    setFormState((current) => ({ ...current, [field]: value }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    setRegistration(formState);
    navigate("/permissions");
  }

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">Registration</p>
        <h1>Collect basic candidate details</h1>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label className="form-field">
            <span>Full name</span>
            <input
              value={formState.full_name}
              onChange={(event) => handleChange("full_name", event.target.value)}
              required
            />
          </label>
          <label className="form-field">
            <span>District</span>
            <input
              value={formState.district}
              onChange={(event) => handleChange("district", event.target.value)}
              required
            />
          </label>
          <label className="form-field">
            <span>Role applied</span>
            <select
              value={formState.role_applied}
              onChange={(event) => handleChange("role_applied", event.target.value)}
              required
            >
              <option value="Electrician">Electrician</option>
              <option value="Delivery Associate">Delivery Associate</option>
              <option value="Plumber">Plumber</option>
              <option value="Welder">Welder</option>
            </select>
          </label>
          <label className="form-field">
            <span>Interview Language</span>
            <select
              value={formState.language}
              onChange={(event) => handleChange("language", event.target.value)}
              required
            >
              <option value="en">English (English)</option>
              <option value="hi">Hindi (हिंदी)</option>
              <option value="kn">Kannada (ಕನ್ನಡ)</option>
            </select>
          </label>
          <label className="form-field">
            <span>Phone number</span>
            <input
              value={formState.phone_number}
              onChange={(event) => handleChange("phone_number", event.target.value)}
            />
          </label>
          <div className="button-row">
            <button type="button" className="button button-secondary" onClick={() => navigate("/")}>
              Back
            </button>
            <button type="submit" className="button button-primary">
              Continue
            </button>
          </div>
        </form>
      </section>
    </main>
  );
}

export default Registration;

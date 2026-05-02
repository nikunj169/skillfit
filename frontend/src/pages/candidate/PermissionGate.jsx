import { useNavigate } from "react-router-dom";
import { useMediaRecorder } from "../../hooks/useMediaRecorder";

function PermissionGate() {
  const navigate = useNavigate();
  const { permissionState, requestPermissions } = useMediaRecorder();

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">Permissions</p>
        <h1>Prepare device access</h1>
        <p className="lede">
          The final product will use camera and microphone capture. This starter flow asks for permissions and
          then continues with transcript-based responses.
        </p>

        <div className="button-row">
          <button type="button" className="button button-primary" onClick={requestPermissions}>
            Request Camera and Mic
          </button>
          <button type="button" className="button button-secondary" onClick={() => navigate("/interview")}>
            Continue Anyway
          </button>
        </div>

        <p className="inline-status">Permission status: {permissionState}</p>

        <button type="button" className="button button-primary" onClick={() => navigate("/interview")}>
          Start Interview
        </button>
      </section>
    </main>
  );
}

export default PermissionGate;

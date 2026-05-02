import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import AIVoicePrompt from "../../components/AIVoicePrompt";
import ProgressStepper from "../../components/ProgressStepper";
import VideoRecorder from "../../components/VideoRecorder";
import { useInterviewSession } from "../../hooks/useInterviewSession";
import { useSessionContext } from "../../context/SessionContext";

function Interview() {
  const navigate = useNavigate();
  const { registration, session } = useSessionContext();
  const { beginSession, sendChunk, questions, loading, error } = useInterviewSession();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [responseText, setResponseText] = useState("");
  const hasStartedRef = useRef(false);

  useEffect(() => {
    async function ensureSession() {
      if (!session && !hasStartedRef.current) {
        hasStartedRef.current = true;
        await beginSession();
      }
    }

    ensureSession();
  }, [beginSession, session]);

  const currentQuestion = questions[currentIndex];

  async function handleNext() {
    if (!currentQuestion || !responseText.trim()) {
      return;
    }

    await sendChunk(currentQuestion.id, responseText.trim());
    setResponseText("");

    if (currentIndex === questions.length - 1) {
      navigate("/processing");
      return;
    }

    setCurrentIndex((index) => index + 1);
  }

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">Interview</p>
        <h1>{registration.role_applied || "Candidate"} interview</h1>
        <ProgressStepper currentStep={currentIndex + 1} totalSteps={Math.max(questions.length, 3)} />
        {currentQuestion ? (
          <>
            <AIVoicePrompt question={currentQuestion.text} language={registration.language} />
            <VideoRecorder responseText={responseText} onChange={setResponseText} disabled={loading} />
            {error ? <p className="error-text">{error}</p> : null}
            <div className="button-row">
              <button type="button" className="button button-secondary" onClick={() => navigate("/")}>
                Exit
              </button>
              <button type="button" className="button button-primary" onClick={handleNext} disabled={loading}>
                {currentIndex === questions.length - 1 ? "Finish Interview" : "Submit and Continue"}
              </button>
            </div>
          </>
        ) : (
          <p className="inline-status">Loading question set...</p>
        )}
      </section>
    </main>
  );
}

export default Interview;

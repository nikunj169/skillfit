import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import AIVoicePrompt from "../../components/AIVoicePrompt";
import ProgressStepper from "../../components/ProgressStepper";
import VideoRecorder from "../../components/VideoRecorder";
import { useInterviewSession } from "../../hooks/useInterviewSession";
import { useMediaRecorder } from "../../hooks/useMediaRecorder";
import { useSessionContext } from "../../context/SessionContext";

function Interview() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { registration, session } = useSessionContext();
  const { beginSession, sendChunk, questions, loading, error } = useInterviewSession();
  const { requestPermissions, startRecording, stopRecording, cleanupStream, isRecording, stream } = useMediaRecorder();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [videoBlob, setVideoBlob] = useState(null);
  const hasStartedRef = useRef(false);
  const recordPromiseRef = useRef(null);

  useEffect(() => {
    async function ensureSession() {
      if (!session && !hasStartedRef.current) {
        hasStartedRef.current = true;
        await requestPermissions(true);
        await beginSession();
      }
    }

    ensureSession();
    return () => cleanupStream();
  }, [beginSession, session, requestPermissions, cleanupStream]);

  const currentQuestion = questions[currentIndex];

  const localizedRole = registration.role_applied
    ? t(`registration.roles.${registration.role_applied}`, { defaultValue: registration.role_applied })
    : t("interview.defaultRole");

  function handleStartRecording() {
    setVideoBlob(null);
    recordPromiseRef.current = startRecording();
  }

  async function handleStopRecording() {
    stopRecording();
    if (recordPromiseRef.current) {
      const blob = await recordPromiseRef.current;
      setVideoBlob(blob);
    }
  }

  async function handleNext() {
    if (!currentQuestion || !videoBlob) {
      return;
    }

    await sendChunk(currentQuestion.id, videoBlob);
    setVideoBlob(null);

    if (currentIndex === questions.length - 1) {
      navigate("/processing");
      return;
    }

    setCurrentIndex((index) => index + 1);
  }

  return (
    <main className="screen">
      <section className="panel">
        <p className="eyebrow">{t("interview.eyebrow")}</p>
        <h1>{t("interview.headline", { role: localizedRole })}</h1>
        <ProgressStepper currentStep={currentIndex + 1} totalSteps={Math.max(questions.length, 3)} />
        {currentQuestion ? (
          <>
            <AIVoicePrompt question={currentQuestion.text} language={registration.language} />
            <VideoRecorder
              stream={stream}
              isRecording={isRecording}
              onStart={handleStartRecording}
              onStop={handleStopRecording}
              disabled={loading}
            />
            {videoBlob && !isRecording && (
              <p className="inline-status">{t("interview.recordingSaved")}</p>
            )}
            {error ? <p className="error-text">{error}</p> : null}
            <div className="button-row">
              <button type="button" className="button button-secondary" onClick={() => navigate("/")}>
                {t("interview.buttonExit")}
              </button>
              <button
                type="button"
                className="button button-primary"
                onClick={handleNext}
                disabled={loading || !videoBlob || isRecording}
              >
                {currentIndex === questions.length - 1
                  ? t("interview.buttonSubmitFinish")
                  : t("interview.buttonSubmitContinue")}
              </button>
            </div>
          </>
        ) : (
          <p className="inline-status">{t("interview.loadingQuestions")}</p>
        )}
      </section>
    </main>
  );
}

export default Interview;

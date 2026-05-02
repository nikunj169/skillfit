import { useEffect, useState } from "react";
import {
  finalizeInterview,
  getQuestionSet,
  startInterviewSession,
  submitInterviewChunk,
} from "../services/interview.service";
import { useSessionContext } from "../context/SessionContext";

export function useInterviewSession() {
  const {
    registration,
    session,
    setSession,
    questions,
    setQuestions,
  } = useSessionContext();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadQuestions() {
      if (!registration.role_applied || questions.length > 0) {
        return;
      }

      try {
        const data = await getQuestionSet(registration.role_applied, registration.language);
        setQuestions(data.questions);
      } catch (requestError) {
        setError(requestError.message || "Unable to load questions.");
      }
    }

    loadQuestions();
  }, [questions.length, registration.language, registration.role_applied, setQuestions]);

  async function beginSession() {
    setLoading(true);
    setError("");
    try {
      const createdSession = await startInterviewSession(registration);
      setSession(createdSession);
      return createdSession;
    } catch (requestError) {
      setError(requestError.message || "Unable to start session.");
      throw requestError;
    } finally {
      setLoading(false);
    }
  }

  async function sendChunk(promptId, videoBlob) {
    if (!session) {
      throw new Error("Interview session has not started yet.");
    }

    setLoading(true);
    setError("");
    try {
      return await submitInterviewChunk({
        session_token: session.session_token,
        prompt_id: promptId,
        language: registration.language,
        videoBlob,
      });
    } catch (requestError) {
      setError(requestError.message || "Unable to submit answer.");
      throw requestError;
    } finally {
      setLoading(false);
    }
  }

  async function finishSession() {
    if (!session) {
      throw new Error("Interview session has not started yet.");
    }

    setLoading(true);
    setError("");
    try {
      return await finalizeInterview({
        session_token: session.session_token,
        role_applied: registration.role_applied,
        language: registration.language,
      });
    } catch (requestError) {
      setError(requestError.message || "Unable to finalize interview.");
      throw requestError;
    } finally {
      setLoading(false);
    }
  }

  return {
    beginSession,
    sendChunk,
    finishSession,
    questions,
    loading,
    error,
  };
}

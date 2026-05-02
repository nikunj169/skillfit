import api from "./api";

export async function startInterviewSession(payload) {
  const response = await api.post("/interview/session/start", payload);
  return response.data;
}

export async function submitInterviewChunk(payload) {
  const formData = new FormData();
  formData.append("session_token", payload.session_token);
  formData.append("prompt_id", payload.prompt_id);
  formData.append("language", payload.language);
  formData.append("video", payload.videoBlob, "chunk.webm");

  const response = await api.post("/interview/session/submit-chunk", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
}

export async function finalizeInterview(payload) {
  const response = await api.post("/interview/session/finalize", payload);
  return response.data;
}

export async function getInterviewStatus(sessionId) {
  const response = await api.get(`/interview/session/${sessionId}/status`);
  return response.data;
}

export async function getQuestionSet(role, language) {
  const response = await api.get(`/interview/questions/${encodeURIComponent(role)}/${language}`);
  return response.data;
}

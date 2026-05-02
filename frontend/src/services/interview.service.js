import api from "./api";

export async function startInterviewSession(payload) {
  const response = await api.post("/interview/session/start", payload);
  return response.data;
}

export async function submitInterviewChunk(payload) {
  const response = await api.post("/interview/session/submit-chunk", payload);
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

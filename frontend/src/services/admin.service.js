import api, { setAdminToken } from "./api";

export async function loginAdmin(credentials) {
  const response = await api.post("/admin/login", credentials);
  const token = response.data.token;
  setAdminToken(token);
  return response.data;
}

export async function getCandidates() {
  const response = await api.get("/admin/candidates");
  return response.data;
}

export async function getCandidateDetail(candidateId) {
  const response = await api.get(`/admin/candidates/${candidateId}`);
  return response.data;
}

export async function updateCandidateStatus(candidateId, action) {
  const response = await api.patch(`/admin/candidates/${candidateId}/status`, {
    action,
  });
  return response.data;
}

export async function getAdminStats() {
  const response = await api.get("/admin/stats");
  return response.data;
}

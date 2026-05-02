import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export function setAdminToken(token) {
  if (token) {
    api.defaults.headers.common["X-Admin-Token"] = token;
  } else {
    delete api.defaults.headers.common["X-Admin-Token"];
  }
}

export default api;

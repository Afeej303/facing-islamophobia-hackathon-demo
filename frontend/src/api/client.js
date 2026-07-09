export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";
export const API_LOAD_ERROR =
  "Live crawler data is unavailable. This feature needs the Linux worker stack: Redis, Celery workers, Celery Beat, Playwright browser workers, Prometheus, and Grafana. Vercel can host this frontend, but it cannot run those long-running services.";

const parse = async (response) => {
  if (!response.ok) {
    let message = await response.text();
    try {
      const parsed = JSON.parse(message);
      message = parsed.detail || message;
    } catch {
      // Keep the raw response text.
    }
    throw new Error(message || "Request failed");
  }
  return response.json();
};

const request = (path, options) =>
  fetch(`${API_BASE}${path}`, options)
    .then(parse)
    .catch((error) => {
      throw new Error(error.message || API_LOAD_ERROR);
    });

export const getAccounts = () => request("/accounts");
export const getComments = (accountId) => request(`/accounts/${accountId}/comments`);
export const getStats = () => request("/stats");
export const analyzeComment = (payload) =>
  request("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
export const getShieldLog = () => request("/shield/log");
export const hideComment = (payload) =>
  request("/shield/hide", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
export const getFacebookStatus = () => request("/facebook/status");
export const getFacebookLoginUrl = () => request("/facebook/login-url");

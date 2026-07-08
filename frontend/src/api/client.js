const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

const parse = async (response) => {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json();
};

export const getAccounts = () => fetch(`${BASE}/accounts`).then(parse);
export const getComments = (accountId) => fetch(`${BASE}/accounts/${accountId}/comments`).then(parse);
export const getStats = () => fetch(`${BASE}/stats`).then(parse);
export const analyzeComment = (payload) =>
  fetch(`${BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then(parse);
export const getShieldLog = () => fetch(`${BASE}/shield/log`).then(parse);
export const hideComment = (payload) =>
  fetch(`${BASE}/shield/hide`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then(parse);
export const getFacebookStatus = () => fetch(`${BASE}/facebook/status`).then(parse);
export const getFacebookLoginUrl = () => fetch(`${BASE}/facebook/login-url`).then(parse);

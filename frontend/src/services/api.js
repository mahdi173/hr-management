const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function fetchWrapper(endpoint, options = {}) {
  const token = localStorage.getItem("timeapp_token");

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`,
      );
    }

    if (response.status === 204) return {};
    return await response.json();
  } catch (error) {
    console.error("API Fetch Error:", error);
    throw error;
  }
}

export const api = {
  get: (endpoint) => fetchWrapper(endpoint, { method: "GET" }),
  post: (endpoint, body) =>
    fetchWrapper(endpoint, { method: "POST", body: JSON.stringify(body) }),
  put: (endpoint, body) =>
    fetchWrapper(endpoint, { method: "PUT", body: JSON.stringify(body) }),
  delete: (endpoint) => fetchWrapper(endpoint, { method: "DELETE" }),
};

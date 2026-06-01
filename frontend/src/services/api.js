const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function fetchWrapper(endpoint, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
    ...options.headers,
  };

  const config = {
    ...options,
    headers,
    credentials: "include",
  };

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, config);

    if (!response.ok) {
      if (
        response.status === 401 &&
        window.location.pathname !== "/" &&
        window.location.pathname !== "/login"
      ) {
        window.location.href = "/login";
      }

      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
          errorData.message ||
          `HTTP error! status: ${response.status}`,
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

  patch: (endpoint, body) =>
    fetchWrapper(endpoint, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : null,
    }),

  delete: (endpoint) => fetchWrapper(endpoint, { method: "DELETE" }),
};

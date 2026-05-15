const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://technogym-redesign-api.onrender.com/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const message = payload?.detail || payload?.message || "Something went wrong. Please try again.";
    throw new Error(message);
  }

  return payload;
}

export const api = {
  getCategories: () => request("/categories"),
  getProducts: () => request("/products"),
  createInquiry: (data) =>
    request("/inquiries", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  createOrder: (data) =>
    request("/orders", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

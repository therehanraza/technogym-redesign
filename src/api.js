const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://technogym-redesign-api.onrender.com/api";

function withParams(path, params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, value);
    }
  });
  const suffix = query.toString();
  return suffix ? `${path}?${suffix}` : path;
}

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
  getHealth: () => request("/health"),
  getSite: () => request("/site"),
  getNavigation: () => request("/navigation"),
  getPage: (path) => request(withParams("/page", { path })),
  getPages: () => request("/pages"),
  getCategories: () => request("/categories"),
  getCategory: (slug) => request(`/categories/${slug}`),
  getProducts: (params) => request(withParams("/products", params)),
  getProduct: (slug) => request(`/products/${slug}`),
  getInquiries: () => request("/inquiries"),
  getOrders: () => request("/orders"),
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

import apiClient from "./client";

export async function signup(name, email, password) {
  const response = await apiClient.post("/users", { name, email, password });
  return response.data;
}

export async function login(email, password) {
  // Our backend's /login route expects form-encoded data, not JSON
  const formData = new URLSearchParams();
  formData.append("username", email); // backend treats "username" field as email
  formData.append("password", password);

  const response = await apiClient.post("/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  const { access_token } = response.data;
  localStorage.setItem("token", access_token); // save token for future requests
  return access_token;
}

export function logout() {
  localStorage.removeItem("token");
}

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}
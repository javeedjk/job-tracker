import apiClient from "./client";

export async function getApplications() {
  const response = await apiClient.get("/applications");
  return response.data;
}

export async function createApplication(data) {
  const response = await apiClient.post("/applications", data);
  return response.data;
}

export async function updateApplication(id, data) {
  const response = await apiClient.put(`/applications/${id}`, data);
  return response.data;
}

export async function deleteApplication(id) {
  await apiClient.delete(`/applications/${id}`);
}

export async function triggerResearch(id) {
  const response = await apiClient.post(`/applications/${id}/research`);
  return response.data;
}

export async function getResearch(id) {
  const response = await apiClient.get(`/applications/${id}/research`);
  return response.data;
}
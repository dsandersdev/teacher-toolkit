import { api } from "./client";

export const resourceApi = {
  async list(query = "") {
    const response = await api.get("/resources/", {
      params: { query },
    });

    return response.data;
  },

  async getByType(resourceType) {
    const response = await api.get(
      `/resources/type/${resourceType}`
    );

    return response.data;
  },

  async get(resourceId) {
    const response = await api.get(`/resources/${resourceId}`);
    return response.data;
  },
};
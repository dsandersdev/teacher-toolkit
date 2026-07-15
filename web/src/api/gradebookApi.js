import { api } from "./client";

export const gradebookApi = {
  async getAssessments(teacherId) {
    const response = await api.get(
      `/gradebook/assessments/${teacherId}`
    );

    return response.data;
  },

  async getResults(assessmentId) {
    const response = await api.get(
      `/gradebook/results/${assessmentId}`
    );

    return response.data;
  },

  async getStudentsNeedingSupport(
    assessmentId,
    threshold = 70
  ) {
    const response = await api.get(
      `/gradebook/support/${assessmentId}`,
      {
        params: { threshold },
      }
    );

    return response.data;
  },
};
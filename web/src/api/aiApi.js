import { api } from "./client";

export const aiApi = {
  async getTeacherHistory(teacherId) {
    const response = await api.get(
      `/ai/history/teacher/${teacherId}`
    );

    return response.data;
  },

  async getStudentHistory(studentId) {
    const response = await api.get(
      `/ai/history/student/${studentId}`
    );

    return response.data;
  },
};
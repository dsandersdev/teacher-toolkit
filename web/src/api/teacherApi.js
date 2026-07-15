import { api } from "./client";

export const teacherApi = {
  async getTeacher(teacherId) {
    const response = await api.get(`/teachers/${teacherId}`);
    return response.data;
  },

  async getStudents(teacherId) {
    const response = await api.get(`/students/${teacherId}`);
    return response.data;
  },
};
import { api } from "./client";

export const teacherApi = {
  async list() {
    const response = await api.get("/teachers");
    return response.data;
  },

  async getTeacher(teacherId) {
    const response = await api.get(`/teachers/${teacherId}`);
    return response.data;
  },

  async getStudents(teacherId) {
    const response = await api.get(`/students/${teacherId}`);
    return response.data;
  },

  async createStudent(student) {
    const response = await api.post("/students", student);
    return response.data;
  },
};
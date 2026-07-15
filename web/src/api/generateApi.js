import { api } from "./client";

export const generateApi = {
  async lessonPlan({
    teacherId,
    topic,
    grade,
    duration = "45 minutes",
  }) {
    const response = await api.post(
      "/generate/lesson-plan",
      {
        teacher_id: teacherId,
        topic,
        grade,
        duration,
      }
    );

    return response.data;
  },
};
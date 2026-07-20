import { createContext, useContext, useState } from "react";

const TeacherContext = createContext(null);

const DEFAULT_TEACHER_ID = 1;

export function TeacherProvider({ children }) {
  const [teacherId, setTeacherId] = useState(() => {
    const saved = localStorage.getItem("teacherId");

    return saved ? Number(saved) : DEFAULT_TEACHER_ID;
  });

  const [teacher, setTeacher] = useState(null);
  const [teachers, setTeachers] = useState([]);

  function changeTeacher(id) {
    const teacherId = Number(id);

    setTeacherId(teacherId);
    localStorage.setItem("teacherId", teacherId);
  }

  return (
    <TeacherContext.Provider
      value={{
        teacherId,
        setTeacherId: changeTeacher,
        teacher,
        setTeacher,
        teachers,
        setTeachers,
      }}
    >
      {children}
    </TeacherContext.Provider>
  );
}

export function useTeacher() {
  const context = useContext(TeacherContext);

  if (!context) {
    throw new Error(
      "useTeacher must be used inside a TeacherProvider"
    );
  }

  return context;
}
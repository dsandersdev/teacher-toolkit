import { useEffect, useState } from "react";
import { api } from "./api/client";
import "./App.css";

function App() {
  const [teacher, setTeacher] = useState(null);
  const [students, setStudents] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [aiHistory, setAiHistory] = useState([]);

  useEffect(() => {
    async function loadDashboard() {
      const teacherId = 1;

      const teacherResponse = await api.get(`/teachers/${teacherId}`);
      const studentsResponse = await api.get(`/students/${teacherId}`);
      const assessmentsResponse = await api.get(
        `/gradebook/assessments/${teacherId}`
      );
      const aiHistoryResponse = await api.get(
        `/ai/history/teacher/${teacherId}`
      );

      setTeacher(teacherResponse.data);
      setStudents(studentsResponse.data);
      setAssessments(assessmentsResponse.data);
      setAiHistory(aiHistoryResponse.data);
    }

    loadDashboard();
  }, []);

  return (
    <main className="dashboard">
      <h1>Teacher Toolkit Dashboard</h1>

      {teacher && (
        <section className="welcome-card">
          <h2>Welcome {teacher.name}</h2>
          <p>{teacher.school}</p>
        </section>
      )}

      <section className="stats-grid">
        <div className="stat-card">
          <h3>Students</h3>
          <p>{students.length}</p>
        </div>

        <div className="stat-card">
          <h3>Assessments</h3>
          <p>{assessments.length}</p>
        </div>

        <div className="stat-card">
          <h3>AI Records</h3>
          <p>{aiHistory.length}</p>
        </div>
      </section>

      <section className="panel">
        <h2>Students</h2>

        {students.map((student) => (
          <div className="list-row" key={student.id}>
            {student.first_name} {student.last_name}
          </div>
        ))}
      </section>

      <section className="panel">
        <h2>Recent AI History</h2>

        {aiHistory.slice(0, 5).map((item) => (
          <div className="list-row" key={item.id}>
            <strong>{item.history_type}</strong>
            <br />
            {item.created_at}
          </div>
        ))}
      </section>
    </main>
  );
}

export default App;
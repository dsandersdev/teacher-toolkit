import { useEffect, useState } from "react";
import { api } from "./api/client";
import "./App.css";

function App() {
  const [activeSection, setActiveSection] = useState("dashboard");
  const [teacher, setTeacher] = useState(null);
  const [students, setStudents] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [aiHistory, setAiHistory] = useState([]);
  const [resources, setResources] = useState([]);
  const [resourceFilter, setResourceFilter] = useState("");
  const [selectedResource, setSelectedResource] = useState(null);
  const [lessonTopic, setLessonTopic] = useState("");
  const [lessonGrade, setLessonGrade] = useState("2");
  const [generating, setGenerating] = useState(false);
  const teacherId = 1;

  useEffect(() => {
    async function loadDashboard() {
      const teacherResponse = await api.get(`/teachers/${teacherId}`);
      const studentsResponse = await api.get(`/students/${teacherId}`);
      const resourcesResponse = await api.get("/resources/");
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
      setResources(resourcesResponse.data);
    }

    loadDashboard();
  }, []);

  async function generateLesson() {
    setGenerating(true);

    const response = await api.post(
      "/generate/lesson-plan",
      {
        teacher_id: teacherId,
        topic: lessonTopic,
        grade: lessonGrade,
        duration: "45 minutes",
      }
    );

    setResources([
      response.data,
      ...resources,
    ]);

    setLessonTopic("");
    setGenerating(false);
  }

  return (
    <main className="dashboard">
      <h1>Teacher Toolkit</h1>

      <nav className="nav-tabs">
        <button onClick={() => setActiveSection("dashboard")}>Dashboard</button>
        <button onClick={() => setActiveSection("students")}>Students</button>
        <button onClick={() => setActiveSection("gradebook")}>Gradebook</button>
        <button onClick={() => setActiveSection("resources")}>Resources</button>
        <button onClick={() => setActiveSection("generate")}>Generate</button>
        <button onClick={() => setActiveSection("ai")}>AI History</button>
      </nav>

      {teacher && (
        <section className="welcome-card">
          <h2>Welcome {teacher.name}</h2>
          <p>{teacher.school}</p>
        </section>
      )}

      {activeSection === "dashboard" && (
        <>
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
        </>
      )}

      {activeSection === "students" && (
        <section className="panel">
          <h2>Students</h2>

          {students.map((student) => (
            <div className="list-row" key={student.id}>
              {student.first_name} {student.last_name}
            </div>
          ))}
        </section>
      )}

      {activeSection === "gradebook" && (
        <section className="panel">
          <h2>Assessments</h2>

          {assessments.map((assessment) => (
            <div className="list-row" key={assessment.id}>
              <strong>{assessment.title}</strong>
              <br />
              Type: {assessment.assessment_type}
              <br />
              Max Score: {assessment.max_score}
            </div>
          ))}
        </section>
      )}

      {activeSection === "resources" && (
        <section className="panel">
          <h2>Resources</h2>

          <div className="filter-buttons">
            <button onClick={() => setResourceFilter("")}>All</button>
            <button onClick={() => setResourceFilter("lesson_plan")}>
              Lesson Plans
            </button>
            <button onClick={() => setResourceFilter("worksheet")}>
              Worksheets
            </button>
            <button onClick={() => setResourceFilter("quiz")}>
              Quizzes
            </button>
            <button onClick={() => setResourceFilter("intervention")}>
              Interventions
            </button>
          </div>
        {resources
          .filter((resource) => {
            if (!resourceFilter) {
              return true;
            }

            return resource.type === resourceFilter;
          })
          .map((resource) => (
          <div className="list-row" key={resource.id}>
            <strong>{resource.title || "Untitled Resource"}</strong>
            <br />
            Type: {resource.type}
            <br />
            Created: {resource.created_at}
            <br />

            <button
              className="open-button"
              onClick={() => setSelectedResource(resource)}
            >
              Open
            </button>
          </div>
          ))}
          {selectedResource && (
            <div className="resource-viewer">
              <button
                className="close-button"
                onClick={() => setSelectedResource(null)}
              >
                Close
              </button>

              <h3>{selectedResource.title || "Untitled Resource"}</h3>

              <p>
                <strong>Type:</strong> {selectedResource.type}
              </p>

              <pre>{selectedResource.content}</pre>
            </div>
          )}
        </section>
      )}

      {activeSection === "generate" && (
        <section className="panel">
          <h2>Create Lesson Plan</h2>

          <input
            placeholder="Topic"
            value={lessonTopic}
            onChange={(e) => setLessonTopic(e.target.value)}
          />

          <input
            placeholder="Grade"
            value={lessonGrade}
            onChange={(e) => setLessonGrade(e.target.value)}
          />

          <button
            onClick={generateLesson}
            disabled={generating}
          >
            {generating
              ? "Generating..."
              : "Generate Lesson"}
          </button>
        </section>
      )}

      {activeSection === "ai" && (
        <section className="panel">
          <h2>AI History</h2>

          {aiHistory.map((item) => (
            <div className="list-row" key={item.id}>
              <strong>{item.history_type}</strong>
              <br />
              {item.created_at}
              <br />
              {item.response?.slice(0, 250)}
            </div>
          ))}
        </section>
      )}
    </main>
  );
}

export default App;
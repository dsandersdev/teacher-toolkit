import { useEffect, useState } from "react";
import { api } from "./api/client";
import "./App.css";
import Navigation from "./components/Navigation";
import Dashboard from "./components/Dashboard";
import Students from "./components/Students";
import Gradebook from "./components/Gradebook";
import AIHistory from "./components/AIHistory";
import Generator from "./components/Generator";
import Resources from "./components/Resources";


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

      <Navigation
        activeSection={activeSection}
        onSectionChange={setActiveSection}
      />
      {teacher && (
        <section className="welcome-card">
          <h2>Welcome {teacher.name}</h2>
          <p>{teacher.school}</p>
        </section>
      )}

      {activeSection === "dashboard" && (
        <Dashboard
          students={students}
          assessments={assessments}
          aiHistory={aiHistory}
        />
      )}

      {activeSection === "students" && (
        <Students students={students} />
      )}

      {activeSection === "gradebook" && (
        <Gradebook assessments={assessments} />
      )}

      {activeSection === "resources" && (
        <Resources
          resources={resources}
          resourceFilter={resourceFilter}
          selectedResource={selectedResource}
          onFilterChange={setResourceFilter}
          onSelectResource={setSelectedResource}
          onCloseResource={() => setSelectedResource(null)}
        />
      )} 

      {activeSection === "generate" && (
        <Generator
          lessonTopic={lessonTopic}
          lessonGrade={lessonGrade}
          generating={generating}
          onTopicChange={setLessonTopic}
          onGradeChange={setLessonGrade}
          onGenerate={generateLesson}
        />
      )}

      {activeSection === "ai" && (
        <AIHistory aiHistory={aiHistory} />
      )}
    </main>
  );
}

export default App;
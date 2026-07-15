import { useEffect, useState } from "react";
import { teacherApi } from "./api/teacherApi";
import { resourceApi } from "./api/resourceApi";
import { gradebookApi } from "./api/gradebookApi";
import { aiApi } from "./api/aiApi";
import { generateApi } from "./api/generateApi";
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
      const [
        teacherData,
        studentsData,
        resourcesData,
        assessmentsData,
        aiHistoryData,
      ] = await Promise.all([
        teacherApi.getTeacher(teacherId),
        teacherApi.getStudents(teacherId),
        resourceApi.list(),
        gradebookApi.getAssessments(teacherId),
        aiApi.getTeacherHistory(teacherId),
      ]);

      setTeacher(teacherData);
      setStudents(studentsData);
      setResources(resourcesData);
      setAssessments(assessmentsData);
      setAiHistory(aiHistoryData);
    }

    loadDashboard();
  }, []);

    async function generateLesson() {
      if (!lessonTopic.trim()) {
        return;
      }

      setGenerating(true);

      try {
        const resource = await generateApi.lessonPlan({
          teacherId,
          topic: lessonTopic.trim(),
          grade: lessonGrade.trim(),
        });

        setResources((currentResources) => [
          resource,
          ...currentResources,
        ]);

        setLessonTopic("");
        setSelectedResource(resource);
        setActiveSection("resources");
      } catch (error) {
        console.error("Lesson generation failed:", error);
      } finally {
        setGenerating(false);
      }
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
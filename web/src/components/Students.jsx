import { useState } from "react";
import Card from "./ui/Card";
import Button from "./ui/Button";
import EmptyState from "./ui/EmptyState";

export default function Students({
  students,
  onAddStudent,
}) {
  const [studentName, setStudentName] = useState("");
  const [adding, setAdding] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    const name = studentName.trim();

    if (!name) {
      return;
    }

    setAdding(true);

    try {
      await onAddStudent(name);
      setStudentName("");
    } finally {
      setAdding(false);
    }
  }

  return (
    <Card title="Students">
      <form onSubmit={handleSubmit}>
        <label htmlFor="student-name">
          Student name
        </label>

        <input
          id="student-name"
          type="text"
          value={studentName}
          onChange={(event) =>
            setStudentName(event.target.value)
          }
          placeholder="Enter student name"
          disabled={adding}
        />

        <Button
          type="submit"
          disabled={adding || !studentName.trim()}
        >
          {adding ? "Adding..." : "Add Student"}
        </Button>
      </form>

      {!students.length ? (
        <EmptyState
          title="No students yet"
          message="Add students to begin tracking grades, progress, and interventions."
        />
      ) : (
      <ul>
        {students.map((student) => {
          const fullName = [
            student.first_name,
            student.last_name,
          ]
            .filter(Boolean)
            .join(" ");

          return (
            <li key={student.id}>
              {fullName}
            </li>
          );
        })}
      </ul>
      )}
    </Card>
  );
}
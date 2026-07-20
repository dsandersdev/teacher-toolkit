export default function TeacherSelector({
  teachers,
  teacherId,
  onTeacherChange,
}) {
  if (!teachers.length) {
    return null;
  }

  return (
    <div className="teacher-selector">
      <label htmlFor="teacher-select">
        Teacher
      </label>

      <select
        id="teacher-select"
        value={teacherId}
        onChange={(event) =>
          onTeacherChange(Number(event.target.value))
        }
      >
        {teachers.map((teacher) => (
          <option
            key={teacher.id}
            value={teacher.id}
          >
            {teacher.name} — {teacher.school}
          </option>
        ))}
      </select>
    </div>
  );
}
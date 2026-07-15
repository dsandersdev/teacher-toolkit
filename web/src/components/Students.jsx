function Students({ students }) {
  return (
    <section className="panel">
      <h2>Students</h2>

      {students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        students.map((student) => (
          <div className="list-row" key={student.id}>
            {student.first_name} {student.last_name}
          </div>
        ))
      )}
    </section>
  );
}

export default Students;
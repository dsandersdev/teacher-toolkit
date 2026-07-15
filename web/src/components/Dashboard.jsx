function Dashboard({ students, assessments, aiHistory }) {
  return (
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
  );
}

export default Dashboard;
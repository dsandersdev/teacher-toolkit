import Card from "./ui/Card";

function Dashboard({ students, assessments, aiHistory }) {
  return (
    <card title="Dashboard">
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
    </card>
  );
}

export default Dashboard;
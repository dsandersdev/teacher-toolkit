function Gradebook({ assessments }) {
  return (
    <section className="panel">
      <h2>Assessments</h2>

      {assessments.length === 0 ? (
        <p>No assessments found.</p>
      ) : (
        assessments.map((assessment) => (
          <div className="list-row" key={assessment.id}>
            <strong>{assessment.title}</strong>

            <br />

            Type: {assessment.assessment_type}

            <br />

            Max Score: {assessment.max_score}
          </div>
        ))
      )}
    </section>
  );
}

export default Gradebook;
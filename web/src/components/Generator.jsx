function Generator({
  lessonTopic,
  lessonGrade,
  generating,
  onTopicChange,
  onGradeChange,
  onGenerate,
}) {
  return (
    <section className="panel">
      <h2>Create Lesson Plan</h2>

      <input
        placeholder="Topic"
        value={lessonTopic}
        onChange={(event) => onTopicChange(event.target.value)}
      />

      <input
        placeholder="Grade"
        value={lessonGrade}
        onChange={(event) => onGradeChange(event.target.value)}
      />

      <button onClick={onGenerate} disabled={generating}>
        {generating ? "Generating..." : "Generate Lesson"}
      </button>
    </section>
  );
}

export default Generator;
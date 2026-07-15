function AIHistory({ aiHistory }) {
  return (
    <section className="panel">
      <h2>AI History</h2>

      {aiHistory.length === 0 ? (
        <p>No AI history found.</p>
      ) : (
        aiHistory.map((item) => (
          <div className="list-row" key={item.id}>
            <strong>{item.history_type}</strong>
            <br />
            {item.created_at}
            <br />
            {item.response?.slice(0, 250)}
          </div>
        ))
      )}
    </section>
  );
}

export default AIHistory;
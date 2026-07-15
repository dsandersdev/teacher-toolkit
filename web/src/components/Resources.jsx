function Resources({
  resources,
  resourceFilter,
  selectedResource,
  onFilterChange,
  onSelectResource,
  onCloseResource,
}) {
  const filteredResources = resources.filter((resource) => {
    if (!resourceFilter) {
      return true;
    }

    return resource.type === resourceFilter;
  });

  return (
    <section className="panel">
      <h2>Resources</h2>

      <div className="filter-buttons">
        <button onClick={() => onFilterChange("")}>All</button>

        <button onClick={() => onFilterChange("lesson_plan")}>
          Lesson Plans
        </button>

        <button onClick={() => onFilterChange("worksheet")}>
          Worksheets
        </button>

        <button onClick={() => onFilterChange("quiz")}>
          Quizzes
        </button>

        <button onClick={() => onFilterChange("intervention")}>
          Interventions
        </button>
      </div>

      {filteredResources.length === 0 ? (
        <p>No resources found.</p>
      ) : (
        filteredResources.map((resource) => (
          <div className="list-row" key={resource.id}>
            <strong>{resource.title || "Untitled Resource"}</strong>

            <br />

            Type: {resource.type}

            <br />

            Created: {resource.created_at}

            <br />

            <button
              className="open-button"
              onClick={() => onSelectResource(resource)}
            >
              Open
            </button>
          </div>
        ))
      )}

      {selectedResource && (
        <div className="resource-viewer">
          <button
            className="close-button"
            onClick={onCloseResource}
          >
            Close
          </button>

          <h3>
            {selectedResource.title || "Untitled Resource"}
          </h3>

          <p>
            <strong>Type:</strong> {selectedResource.type}
          </p>

          <pre>{selectedResource.content}</pre>
        </div>
      )}
    </section>
  );
}

export default Resources;
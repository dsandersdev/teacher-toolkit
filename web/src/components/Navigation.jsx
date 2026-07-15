function Navigation({ activeSection, onSectionChange }) {
  const sections = [
    { id: "dashboard", label: "Dashboard" },
    { id: "students", label: "Students" },
    { id: "gradebook", label: "Gradebook" },
    { id: "resources", label: "Resources" },
    { id: "generate", label: "Generate" },
    { id: "ai", label: "AI History" },
  ];

  return (
    <nav className="nav-tabs">
      {sections.map((section) => (
        <button
          key={section.id}
          className={activeSection === section.id ? "active" : ""}
          onClick={() => onSectionChange(section.id)}
        >
          {section.label}
        </button>
      ))}
    </nav>
  );
}

export default Navigation;
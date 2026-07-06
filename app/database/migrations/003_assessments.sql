CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    resource_id INTEGER,
    title TEXT NOT NULL,
    assessment_type TEXT,
    max_score REAL DEFAULT 100,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(teacher_id)
    REFERENCES teachers(id),

    FOREIGN KEY(resource_id)
    REFERENCES resources(id)
);
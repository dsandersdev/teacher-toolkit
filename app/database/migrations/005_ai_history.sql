CREATE TABLE IF NOT EXISTS ai_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    student_id INTEGER,
    resource_id INTEGER,
    assessment_id INTEGER,
    history_type TEXT NOT NULL,
    prompt TEXT,
    response TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(teacher_id)
    REFERENCES teachers(id),

    FOREIGN KEY(student_id)
    REFERENCES students(id),

    FOREIGN KEY(resource_id)
    REFERENCES resources(id),

    FOREIGN KEY(assessment_id)
    REFERENCES assessments(id)
);
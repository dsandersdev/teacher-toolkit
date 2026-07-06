CREATE TABLE IF NOT EXISTS student_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    assessment_id INTEGER,
    score REAL NOT NULL,
    percent REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(student_id)
    REFERENCES students(id),

    FOREIGN KEY(assessment_id)
    REFERENCES assessments(id)
);
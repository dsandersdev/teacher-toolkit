CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT,
    grade_level TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(teacher_id)
    REFERENCES teachers(id)
);
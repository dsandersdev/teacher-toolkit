CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    school TEXT,
    curriculum TEXT,
    teaching_style TEXT
);


CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    type TEXT NOT NULL,
    title TEXT,
    content TEXT,
    created_at TEXT,

    FOREIGN KEY(teacher_id)
    REFERENCES teachers(id)
);


CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER,
    target_id INTEGER,
    relationship_type TEXT
);
import sqlite3
from pathlib import Path


class Database:
    def __init__(
        self,
        db_path="teacher_toolkit.db",
    ):
        self.db_path = Path(db_path)

    def connect(self):
        connection = sqlite3.connect(
            self.db_path
        )

        connection.row_factory = sqlite3.Row

        return connection

    def initialize(self):
        with self.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    school TEXT,
                    curriculum TEXT,
                    teaching_style TEXT
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id INTEGER,
                    type TEXT NOT NULL,
                    title TEXT,
                    content TEXT,
                    created_at TEXT,

                    FOREIGN KEY(teacher_id)
                    REFERENCES teachers(id)
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER,
                    target_id INTEGER,
                    relationship_type TEXT
                )
                """
            )

            connection.commit()
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
        from app.database.migrations import MigrationRunner

        runner = MigrationRunner(self)
        runner.run()
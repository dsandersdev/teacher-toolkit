from pathlib import Path


class MigrationRunner:
    def __init__(self, database):
        self.database = database
        self.migrations_dir = Path(__file__).parent / "migrations"

    def run(self):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL UNIQUE,
                    applied_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            for path in sorted(self.migrations_dir.glob("*.sql")):
                cursor.execute(
                    """
                    SELECT filename
                    FROM schema_migrations
                    WHERE filename = ?
                    """,
                    (path.name,),
                )

                if cursor.fetchone():
                    continue

                sql = path.read_text(encoding="utf-8")
                cursor.executescript(sql)

                cursor.execute(
                    """
                    INSERT INTO schema_migrations (filename)
                    VALUES (?)
                    """,
                    (path.name,),
                )

            connection.commit()
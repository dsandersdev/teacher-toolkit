import sqlite3
from pathlib import Path


DATABASE_PATH = Path("teacher_toolkit.db")
KEEP_TEACHER_ID = 1


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH.resolve()}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        connection.execute("BEGIN")

        tables = [
            "ai_history",
            "assessments",
            "resources",
            "students",
        ]

        for table_name in tables:
            cursor.execute(
                f"""
                UPDATE {table_name}
                SET teacher_id = ?
                WHERE teacher_id != ?
                """,
                (
                    KEEP_TEACHER_ID,
                    KEEP_TEACHER_ID,
                ),
            )

            print(
                f"{table_name}: "
                f"{cursor.rowcount} row(s) updated"
            )

        cursor.execute(
            """
            DELETE FROM teachers
            WHERE id != ?
            """,
            (KEEP_TEACHER_ID,),
        )

        print(
            f"teachers: {cursor.rowcount} duplicate row(s) deleted"
        )

        connection.commit()

        print("\nTeacher cleanup completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
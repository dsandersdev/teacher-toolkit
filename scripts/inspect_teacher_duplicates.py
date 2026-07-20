import sqlite3
from pathlib import Path


DATABASE_PATH = Path("teacher_toolkit.db")


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH.resolve()}"
        )

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        teachers = cursor.execute(
            """
            SELECT id, name, school
            FROM teachers
            ORDER BY id
            """
        ).fetchall()

        print("\nTeachers")
        print("=" * 60)

        for teacher in teachers:
            print(
                f"ID {teacher['id']}: "
                f"{teacher['name']} | {teacher['school']}"
            )

        tables = cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        print("\nTeacher references")
        print("=" * 60)

        for table_row in tables:
            table_name = table_row["name"]

            columns = cursor.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            column_names = {
                column["name"]
                for column in columns
            }

            if "teacher_id" not in column_names:
                continue

            references = cursor.execute(
                f"""
                SELECT teacher_id, COUNT(*) AS total
                FROM "{table_name}"
                GROUP BY teacher_id
                ORDER BY teacher_id
                """
            ).fetchall()

            print(f"\n{table_name}:")

            if not references:
                print("  No teacher references")
                continue

            for reference in references:
                print(
                    f"  Teacher ID {reference['teacher_id']}: "
                    f"{reference['total']} row(s)"
                )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
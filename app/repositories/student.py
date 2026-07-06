class StudentRepository:
    def __init__(self, database):
        self.database = database

    def save(
        self,
        teacher_id: int,
        first_name: str,
        last_name: str = "",
        grade_level: str = "",
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO students
                (
                    teacher_id,
                    first_name,
                    last_name,
                    grade_level
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    teacher_id,
                    first_name,
                    last_name,
                    grade_level,
                ),
            )

            connection.commit()

            return cursor.lastrowid

    def get(self, student_id: int):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE id = ?
                """,
                (student_id,),
            )

            row = cursor.fetchone()

            if not row:
                return None

            return dict(row)

    def list_by_teacher(self, teacher_id: int):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE teacher_id = ?
                ORDER BY last_name, first_name
                """,
                (teacher_id,),
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]
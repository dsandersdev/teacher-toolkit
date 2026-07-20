from app.users.profile import TeacherProfile


class TeacherRepository:
    def __init__(self, database):
        self.database = database

    def save(self, profile: TeacherProfile):
        existing = self.find_by_name(profile.name)

        if existing:
            return existing["id"]

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO teachers
                (
                    name,
                    school,
                    curriculum,
                    teaching_style
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    profile.name,
                    profile.school,
                    profile.curriculum,
                    profile.teaching_style,
                ),
            )

            connection.commit()
            return cursor.lastrowid

    def get(self, teacher_id: int):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM teachers
                WHERE id = ?
                """,
                (teacher_id,),
            )

            row = cursor.fetchone()
            return dict(row) if row else None

    def list_all(self):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM teachers
                ORDER BY name
                """
            )

            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    def find_by_name(self, name: str):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM teachers
                WHERE name = ?
                """,
                (name,),
            )

            row = cursor.fetchone()
            return dict(row) if row else None
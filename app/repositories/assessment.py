class AssessmentRepository:
    def __init__(self, database):
        self.database = database

    def save(
        self,
        teacher_id: int,
        title: str,
        assessment_type: str = "quiz",
        max_score: float = 100,
        resource_id: int | None = None,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO assessments
                (
                    teacher_id,
                    resource_id,
                    title,
                    assessment_type,
                    max_score
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    teacher_id,
                    resource_id,
                    title,
                    assessment_type,
                    max_score,
                ),
            )

            connection.commit()

            return cursor.lastrowid

    def get(self, assessment_id: int):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM assessments
                WHERE id = ?
                """,
                (assessment_id,),
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
                FROM assessments
                WHERE teacher_id = ?
                ORDER BY created_at DESC
                """,
                (teacher_id,),
            )

            return [dict(row) for row in cursor.fetchall()]
class AIHistoryRepository:
    def __init__(self, database):
        self.database = database

    def save(
        self,
        teacher_id: int | None,
        history_type: str,
        response: str,
        prompt: str = "",
        student_id: int | None = None,
        resource_id: int | None = None,
        assessment_id: int | None = None,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO ai_history
                (
                    teacher_id,
                    student_id,
                    resource_id,
                    assessment_id,
                    history_type,
                    prompt,
                    response
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    teacher_id,
                    student_id,
                    resource_id,
                    assessment_id,
                    history_type,
                    prompt,
                    response,
                ),
            )

            connection.commit()
            return cursor.lastrowid

    def list_by_teacher(
        self,
        teacher_id: int,
        history_type: str | None = None,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            if history_type:
                cursor.execute(
                    """
                    SELECT *
                    FROM ai_history
                    WHERE teacher_id = ?
                    AND history_type = ?
                    ORDER BY created_at DESC
                    """,
                    (teacher_id, history_type),
                )
            else:
                cursor.execute(
                    """
                    SELECT *
                    FROM ai_history
                    WHERE teacher_id = ?
                    ORDER BY created_at DESC
                    """,
                    (teacher_id,),
                )

            return [dict(row) for row in cursor.fetchall()]

    def list_by_student(
        self,
        student_id: int,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM ai_history
                WHERE student_id = ?
                ORDER BY created_at DESC
                """,
                (student_id,),
            )

            return [dict(row) for row in cursor.fetchall()]
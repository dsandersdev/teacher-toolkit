class GradebookRepository:
    def __init__(self, database):
        self.database = database

    def record_score(
        self,
        student_id: int,
        assessment_id: int,
        score: float,
        max_score: float,
    ):
        percent = 0

        if score < 0:
            raise ValueError("Score cannot be negative.")

        if max_score <= 0:
            raise ValueError("Max score must be greater than zero.")

        if score > max_score:
            raise ValueError(
                f"Score cannot be greater than max score ({max_score})."
            )
        
        if max_score:
            percent = round((score / max_score) * 100, 2)

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO student_scores
                (
                    student_id,
                    assessment_id,
                    score,
                    percent
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    assessment_id,
                    score,
                    percent,
                ),
            )

            connection.commit()

            return cursor.lastrowid

    def results_for_assessment(self, assessment_id: int):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    student_scores.*,
                    students.first_name,
                    students.last_name
                FROM student_scores
                JOIN students
                ON students.id = student_scores.student_id
                WHERE student_scores.assessment_id = ?
                ORDER BY students.last_name, students.first_name
                """,
                (assessment_id,),
            )

            return [dict(row) for row in cursor.fetchall()]

    def struggling_students(
        self,
        assessment_id: int,
        threshold: float = 70,
    ):
        return [
            row
            for row in self.results_for_assessment(assessment_id)
            if row["percent"] < threshold
        ]
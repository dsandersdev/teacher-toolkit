from app.database.connection import Database
from app.repositories.assessment import AssessmentRepository
from app.repositories.gradebook import GradebookRepository
from app.repositories.student import StudentRepository


def test_gradebook_records_score(tmp_path):
    database = Database(tmp_path / "test.db")
    database.initialize()

    student_repo = StudentRepository(database)
    assessment_repo = AssessmentRepository(database)
    gradebook = GradebookRepository(database)

    student_id = student_repo.save(
        teacher_id=1,
        first_name="Jane",
        last_name="Smith",
        grade_level="2",
    )

    assessment_id = assessment_repo.save(
        teacher_id=1,
        title="Addition Quiz",
        max_score=20,
    )

    gradebook.record_score(
        student_id=student_id,
        assessment_id=assessment_id,
        score=16,
        max_score=20,
    )

    results = gradebook.results_for_assessment(assessment_id)

    assert len(results) == 1
    assert results[0]["percent"] == 80


def test_gradebook_finds_struggling_students(tmp_path):
    database = Database(tmp_path / "test.db")
    database.initialize()

    student_repo = StudentRepository(database)
    assessment_repo = AssessmentRepository(database)
    gradebook = GradebookRepository(database)

    student_id = student_repo.save(
        teacher_id=1,
        first_name="Jane",
        last_name="Smith",
        grade_level="2",
    )

    assessment_id = assessment_repo.save(
        teacher_id=1,
        title="Addition Quiz",
        max_score=20,
    )

    gradebook.record_score(
        student_id=student_id,
        assessment_id=assessment_id,
        score=10,
        max_score=20,
    )

    students = gradebook.struggling_students(
        assessment_id,
        threshold=70,
    )

    assert len(students) == 1
    assert students[0]["first_name"] == "Jane"
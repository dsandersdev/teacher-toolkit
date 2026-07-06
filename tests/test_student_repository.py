from app.database.connection import Database
from app.repositories.student import StudentRepository


def test_student_repository_saves_student(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    database.initialize()

    repo = StudentRepository(database)

    student_id = repo.save(
        teacher_id=1,
        first_name="Jane",
        last_name="Smith",
        grade_level="2",
    )

    student = repo.get(student_id)

    assert student["first_name"] == "Jane"
    assert student["last_name"] == "Smith"
    assert student["grade_level"] == "2"


def test_student_repository_lists_by_teacher(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    database.initialize()

    repo = StudentRepository(database)

    repo.save(
        teacher_id=1,
        first_name="Jane",
        last_name="Smith",
        grade_level="2",
    )

    repo.save(
        teacher_id=2,
        first_name="Other",
        last_name="Student",
        grade_level="3",
    )

    students = repo.list_by_teacher(1)

    assert len(students) == 1
    assert students[0]["first_name"] == "Jane"
from app.database.connection import Database
from app.repositories.teacher import TeacherRepository
from app.users.profile import TeacherProfile


def test_teacher_repository_saves_teacher(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    database.initialize()

    repo = TeacherRepository(database)

    teacher_id = repo.save(
        TeacherProfile(
            name="Test Teacher",
            school="Test School",
        )
    )

    teacher = repo.get(teacher_id)

    assert teacher["name"] == "Test Teacher"
    assert teacher["school"] == "Test School"
from app.database.connection import Database
from app.repositories.assessment import AssessmentRepository


def test_assessment_repository_saves_assessment(tmp_path):
    database = Database(tmp_path / "test.db")
    database.initialize()

    repo = AssessmentRepository(database)

    assessment_id = repo.save(
        teacher_id=1,
        title="Unit 1 Quiz",
        assessment_type="quiz",
        max_score=20,
    )

    assessment = repo.get(assessment_id)

    assert assessment["title"] == "Unit 1 Quiz"
    assert assessment["assessment_type"] == "quiz"
    assert assessment["max_score"] == 20
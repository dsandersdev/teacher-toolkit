from fastapi import APIRouter

from app.database.connection import Database
from app.repositories.assessment import AssessmentRepository
from app.repositories.gradebook import GradebookRepository


router = APIRouter(
    prefix="/gradebook",
    tags=["gradebook"],
)


def get_database():
    return Database()


@router.get("/assessments/{teacher_id}")
def list_assessments(teacher_id: int):
    database = get_database()
    repository = AssessmentRepository(database)
    return repository.list_by_teacher(teacher_id)


@router.get("/results/{assessment_id}")
def assessment_results(assessment_id: int):
    database = get_database()
    repository = GradebookRepository(database)
    return repository.results_for_assessment(assessment_id)


@router.get("/support/{assessment_id}")
def students_needing_support(
    assessment_id: int,
    threshold: float = 70,
):
    database = get_database()
    repository = GradebookRepository(database)
    return repository.struggling_students(
        assessment_id=assessment_id,
        threshold=threshold,
    )
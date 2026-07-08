from fastapi import APIRouter

from app.database.connection import Database
from app.repositories.ai_history import AIHistoryRepository


router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)


def get_repository():
    database = Database()
    return AIHistoryRepository(database)


@router.get("/history/teacher/{teacher_id}")
def teacher_history(
    teacher_id: int,
):
    repository = get_repository()

    return repository.list_by_teacher(
        teacher_id
    )


@router.get("/history/student/{student_id}")
def student_history(
    student_id: int,
):
    repository = get_repository()

    return repository.list_by_student(
        student_id
    )
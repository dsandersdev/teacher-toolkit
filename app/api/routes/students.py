from fastapi import APIRouter

from app.database.connection import Database
from app.repositories.student import StudentRepository

router = APIRouter(
    prefix="/students",
    tags=["students"],
)


def get_repository():
    database = Database()
    return StudentRepository(database)


@router.get("/{teacher_id}")
def list_students(teacher_id: int):
    repository = get_repository()
    return repository.list_by_teacher(teacher_id)
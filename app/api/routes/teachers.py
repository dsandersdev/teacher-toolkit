from fastapi import APIRouter

from app.database.connection import Database
from app.repositories.teacher import TeacherRepository


router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
)


def get_repository():
    database = Database()
    return TeacherRepository(database)


@router.get("")
def list_teachers():
    repository = get_repository()
    return repository.list_all()

@router.get("/{teacher_id}")
def get_teacher(teacher_id: int):
    repository = get_repository()
    return repository.get(teacher_id)
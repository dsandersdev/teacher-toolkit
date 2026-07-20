from fastapi import APIRouter
from pydantic import BaseModel

from app.database.connection import Database
from app.repositories.student import StudentRepository

router = APIRouter(
    prefix="/students",
    tags=["students"],
)


class StudentCreate(BaseModel):
    teacher_id: int
    first_name: str
    last_name: str = ""
    grade_level: str = ""


def get_repository():
    database = Database()
    return StudentRepository(database)


@router.get("/{teacher_id}")
def list_students(teacher_id: int):
    repository = get_repository()
    return repository.list_by_teacher(teacher_id)


@router.post("")
def create_student(student: StudentCreate):
    repository = get_repository()

    return repository.save(
        teacher_id=student.teacher_id,
        first_name=student.first_name,
        last_name=student.last_name,
        grade_level=student.grade_level,
    )
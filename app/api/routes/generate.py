from pydantic import BaseModel
from fastapi import APIRouter

from sdk.ai import AI, AIConfig

from app.config.settings import Settings
from app.database.connection import Database
from app.repositories.resource import ResourceRepository
from app.generators.lesson import LessonGenerator


router = APIRouter(
    prefix="/generate",
    tags=["generate"],
)


class LessonPlanRequest(BaseModel):
    teacher_id: int
    topic: str
    grade: str
    duration: str = "45 minutes"


@router.post("/lesson-plan")
def generate_lesson_plan(request: LessonPlanRequest):
    settings = Settings()
    database = Database()
    database.initialize()

    ai = AI(
        AIConfig(
            provider=settings.ai_provider,
            model=settings.ai_model,
        )
    )

    generator = LessonGenerator(
        ai=ai,
        settings=settings,
    )

    result = generator.generate(
        topic=request.topic,
        grade=request.grade,
        curriculum=getattr(settings, "curriculum", "General elementary curriculum"),
    )

    resource_repository = ResourceRepository(database)

    resource_id = resource_repository.save(
        teacher_id=request.teacher_id,
        resource_type="lesson_plan",
        title=f"Lesson Plan - {request.topic}",
        content=result,
    )

    return {
        "id": resource_id,
        "type": "lesson_plan",
        "title": f"Lesson Plan - {request.topic}",
        "content": result,
    }
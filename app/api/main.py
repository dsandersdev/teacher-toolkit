from fastapi import FastAPI

from app.database.connection import Database
from app.api.routes import students, teachers, resources, gradebook, ai

app = FastAPI(
    title="Teacher Toolkit API",
    version="0.1.0",
)

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(resources.router)
app.include_router(gradebook.router)
app.include_router(ai.router)


@app.on_event("startup")
def startup():
    database = Database()
    database.initialize()


@app.get("/")
def root():
    return {
        "app": "Teacher Toolkit API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }
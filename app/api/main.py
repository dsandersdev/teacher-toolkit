from fastapi import FastAPI

from app.database.connection import Database
from app.api.routes import students, teachers, resources, gradebook, ai, generate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Teacher Toolkit API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(resources.router)
app.include_router(gradebook.router)
app.include_router(ai.router)
app.include_router(generate.router)


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
from fastapi import APIRouter

from app.database.connection import Database
from app.repositories.resource import ResourceRepository


router = APIRouter(
    prefix="/resources",
    tags=["resources"],
)


def get_repository():
    database = Database()
    return ResourceRepository(database)


@router.get("/")
def search_resources(query: str = ""):
    repository = get_repository()
    return repository.search(query)


@router.get("/type/{resource_type}")
def get_resources_by_type(resource_type: str):
    repository = get_repository()
    return repository.find_by_type(resource_type)


@router.get("/{resource_id}")
def get_resource(resource_id: int):
    repository = get_repository()
    return repository.get(resource_id)
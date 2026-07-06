from app.database.connection import Database
from app.repositories.resource import ResourceRepository


def test_resource_repository_saves_resource(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    database.initialize()

    repo = ResourceRepository(database)

    resource_id = repo.save(
        teacher_id=1,
        resource_type="lesson",
        title="Scientific Method",
        content="Steps of the scientific method",
    )

    resource = repo.get(resource_id)

    assert resource["title"] == "Scientific Method"
    assert resource["type"] == "lesson"


def test_resource_repository_search(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    database.initialize()

    repo = ResourceRepository(database)

    repo.save(
        teacher_id=1,
        resource_type="worksheet",
        title="Fractions",
        content="Adding fractions activity",
    )

    results = repo.search("fractions")

    assert len(results) == 1
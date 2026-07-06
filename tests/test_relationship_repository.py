from app.database.connection import Database
from app.repositories.relationship import RelationshipRepository


def test_relationship_repository(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    database.initialize()

    repo = RelationshipRepository(database)

    repo.save(
        source_id=1,
        target_id=2,
        relationship_type="quiz",
    )

    related = repo.find_related(1)

    assert isinstance(related, list)
from app.database.connection import Database


def test_database_initializes(tmp_path):
    db_file = tmp_path / "test.db"

    database = Database(
        db_path=db_file
    )

    database.initialize()

    assert db_file.exists()
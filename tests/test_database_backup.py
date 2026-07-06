from app.database.backup import DatabaseBackup


def test_database_backup_creates_file(tmp_path):
    db_file = tmp_path / "teacher_toolkit.db"
    db_file.write_text("test database", encoding="utf-8")

    backup = DatabaseBackup(
        db_path=db_file,
        backup_dir=tmp_path / "backups",
    )

    backup_path = backup.create_backup()

    assert backup_path.exists()
    assert backup_path.name.startswith("teacher_toolkit_")


def test_database_backup_restores_file(tmp_path):
    db_file = tmp_path / "teacher_toolkit.db"
    db_file.write_text("original", encoding="utf-8")

    backup = DatabaseBackup(
        db_path=db_file,
        backup_dir=tmp_path / "backups",
    )

    backup_path = backup.create_backup()

    db_file.write_text("changed", encoding="utf-8")

    backup.restore_backup(backup_path)

    assert db_file.read_text(encoding="utf-8") == "original"
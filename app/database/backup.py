from datetime import datetime
from pathlib import Path
import shutil


class DatabaseBackup:
    def __init__(
        self,
        db_path="teacher_toolkit.db",
        backup_dir="backups",
    ):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self):
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.db_path}"
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"teacher_toolkit_{timestamp}.db"

        shutil.copy2(
            self.db_path,
            backup_path,
        )

        return backup_path

    def restore_backup(self, backup_path):
        backup_path = Path(backup_path)

        if not backup_path.exists():
            raise FileNotFoundError(
                f"Backup not found: {backup_path}"
            )

        shutil.copy2(
            backup_path,
            self.db_path,
        )

        return self.db_path
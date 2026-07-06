import json
from pathlib import Path

from app.users.profile import TeacherProfile


class ProfileManager:
    def __init__(self, profile_dir="profiles"):
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(exist_ok=True)

    def save(self, profile: TeacherProfile, filename: str | None = None):
        file_name = filename or profile.name
        path = self.profile_dir / f"{file_name}.json"

        path.write_text(
            json.dumps(
                profile.to_dict(),
                indent=2
            ),
            encoding="utf-8",
        )

        return path

    def load(self, name: str):
        path = self.profile_dir / f"{name}.json"

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return TeacherProfile(**data)
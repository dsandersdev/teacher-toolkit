import json
from pathlib import Path

from app.users.profile import TeacherProfile


class ProfileManager:
    def __init__(self, profile_dir="profiles"):
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(exist_ok=True)

        self.active_file = self.profile_dir / "active_profile.json"

    def save(
        self,
        profile: TeacherProfile,
        filename: str | None = None,
    ):
        file_name = filename or self._safe_name(profile.name)

        path = self.profile_dir / f"{file_name}.json"

        path.write_text(
            json.dumps(
                profile.to_dict(),
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def load(self, name: str):
        path = self.profile_dir / f"{name}.json"

        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        return TeacherProfile(**data)

    def list_profiles(self):
        profiles = []

        for path in self.profile_dir.glob("*.json"):
            if path.name == "active_profile.json":
                continue

            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            profiles.append(
                {
                    "file": path.stem,
                    "name": data.get("name", path.stem),
                }
            )

        return profiles

    def set_active(self, profile_file: str):
        self.active_file.write_text(
            json.dumps(
                {
                    "profile": profile_file,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def get_active(self):
        if not self.active_file.exists():
            return None

        data = json.loads(
            self.active_file.read_text(
                encoding="utf-8",
            )
        )

        return self.load(data["profile"])

    def _safe_name(self, name: str):
        return (
            name.lower()
            .replace(" ", "_")
        )
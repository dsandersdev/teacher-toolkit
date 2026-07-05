import json
from pathlib import Path


class ResourceLibrary:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)

    def all(self) -> list[dict]:
        resources = []

        for path in self.output_dir.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_path"] = str(path)
            resources.append(data)

        return sorted(
            resources,
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )

    def find_by_type(self, resource_type: str) -> list[dict]:
        return [
            item
            for item in self.all()
            if item.get("type") == resource_type
        ]
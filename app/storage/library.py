import json
from pathlib import Path


class ResourceLibrary:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)

    def all(self) -> list[dict]:
        resources = []

        for path in self.output_dir.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if "id" not in data:
                data["id"] = path.stem

            if "title" not in data:
                metadata = data.get("metadata", {})
                data["title"] = metadata.get("title", "Untitled")
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

    def search(self, query: str) -> list[dict]:
        query = query.lower().strip()

        if not query:
            return self.all()

        results = []

        for item in self.all():
            metadata = item.get("metadata", {})
            content = item.get("content", "")

            searchable_text = " ".join(
                [
                    item.get("type", ""),
                    metadata.get("title", ""),
                    metadata.get("topic", ""),
                    metadata.get("student_name", ""),
                    metadata.get("situation", ""),
                    metadata.get("grade", ""),
                    metadata.get("curriculum", ""),
                    content,
                ]
            ).lower()

            if query in searchable_text:
                results.append(item)

        return results
import json
import uuid
from datetime import datetime
from pathlib import Path


class MetadataExporter:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save(
        self,
        content: str,
        prefix: str,
        metadata: dict | None = None,
    ) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"{prefix}_{timestamp}.json"

        metadata = metadata or {}

        data = {
            "id": metadata.get("id") or str(uuid.uuid4()),
            "type": prefix,
            "title": metadata.get("title", "Untitled"),
            "created_at": datetime.now().isoformat(),
            "content": content,
            "metadata": metadata,
        }

        output_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        return output_path
from pathlib import Path


class ExportManager:
    def __init__(self, exporters: list):
        self.exporters = exporters

    def save_all(
        self,
        content: str,
        prefix: str,
        metadata: dict | None = None,
    ) -> list[Path]:
        saved_paths = []

        for exporter in self.exporters:
            try:
                path = exporter.save(
                    content,
                    prefix,
                    metadata,
                )
            except TypeError:
                path = exporter.save(
                    content,
                    prefix,
                )

            saved_paths.append(path)

        return saved_paths
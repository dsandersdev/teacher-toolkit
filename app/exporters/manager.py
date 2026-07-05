from pathlib import Path


class ExportManager:
    def __init__(self, exporters: list):
        self.exporters = exporters

    def save_all(self, content: str, prefix: str) -> list[Path]:
        saved_paths = []

        for exporter in self.exporters:
            path = exporter.save(content, prefix)
            saved_paths.append(path)

        return saved_paths
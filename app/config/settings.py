from pathlib import Path

import yaml


class Settings:
    def __init__(self, path: str = "configs/settings.yaml"):
        self.path = Path(path)
        self.data = self.load()

    def load(self) -> dict:
        if not self.path.exists():
            raise FileNotFoundError(
                f"Settings file not found: {self.path}"
            )

        with self.path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    @property
    def ai_provider(self) -> str:
        return self.data["ai"]["provider"]

    @property
    def ai_model(self) -> str:
        return self.data["ai"]["model"]

    @property
    def export_markdown(self) -> bool:
        return self.data["exports"].get("markdown", True)

    @property
    def export_docx(self) -> bool:
        return self.data["exports"].get("docx", True)

    @property
    def school(self) -> str:
        return self.data["teacher"].get(
            "school",
            "",
        )

    @property
    def teaching_style(self) -> str:
        return self.data["teacher"].get(
            "teaching_style",
            "",
        )

    @property
    def default_curriculum(self) -> str:
        return self.data["teacher"].get(
            "default_curriculum",
            "",
        )

    @property
    def tone(self) -> str:
        return self.data["teacher"].get(
            "tone",
            "friendly and professional",
        )
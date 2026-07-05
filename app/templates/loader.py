from pathlib import Path


class TemplateLoader:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)

    def load(self, name: str) -> str:
        path = self.template_dir / name

        if not path.exists():
            raise FileNotFoundError(f"Template not found: {path}")

        return path.read_text(encoding="utf-8")

    def render(self, name: str, values: dict) -> str:
        content = self.load(name)

        for key, value in values.items():
            content = content.replace(
                "{{ " + key + " }}",
                str(value),
            )

        return content
from sdk.ai import AI, AIConfig
from app.exporters.markdown import MarkdownExporter
from app.exporters.docx import DocxExporter
from app.exporters.manager import ExportManager
from app.config.settings import Settings
from app.registry import GENERATOR_REGISTRY

class TeacherToolkit:
    def __init__(self):
        self.settings = Settings()
        self.ai = AI(
            AIConfig(
                provider=self.settings.ai_provider,
                model=self.settings.ai_model,
            )
        )
        self.generators = {
            key: item["class"](self.ai)
            for key, item in GENERATOR_REGISTRY.items()
        }
        exporters = []

        if self.settings.export_markdown:
            exporters.append(MarkdownExporter())

        if self.settings.export_docx:
            exporters.append(DocxExporter())

        self.export_manager = ExportManager(exporters=exporters)


    def finish(
        self,
        content: str,
        prefix: str,
    ):
        print("\n")
        print(content)

        saved_paths = self.export_manager.save_all(
            content,
            prefix,
        )

        print("\nSaved files:")
        for path in saved_paths:
            print(f"- {path}")

def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===")

    for key, item in GENERATOR_REGISTRY.items():
        print(f"{key}. {item['name']}")

    choice = input("\nChoose: ").strip()

    if choice not in GENERATOR_REGISTRY:
        print("Invalid option")
        return

    item = GENERATOR_REGISTRY[choice]
    values = {}

    for field, default in item["fields"].items():
        label = field.replace("_", " ").title()

        if default:
            value = input(
                f"{label} [{default}]: "
            ).strip()

        values[field] = value or default
    else:
        values[field] = input(
            f"{label}: "
        ).strip()
    generator = toolkit.generators[choice]

    result = generator.generate(**values)

    toolkit.finish(
        result,
        item["prefix"],
    )

if __name__ == "__main__":
    main()
from sdk.ai import AI, AIConfig
from app.exporters.markdown import MarkdownExporter
from app.exporters.docx import DocxExporter
from app.exporters.manager import ExportManager
from app.config.settings import Settings
from app.registry import GENERATOR_REGISTRY
from app.exporters.metadata import MetadataExporter
from app.storage.library import ResourceLibrary

class TeacherToolkit:
    def __init__(self):
        self.settings = Settings()
        self.library = ResourceLibrary()
        self.ai = AI(
            AIConfig(
                provider=self.settings.ai_provider,
                model=self.settings.ai_model,
            )
        )
        self.generators = {
            key: item["class"](
            self.ai,
            self.settings,
        )
    for key, item in GENERATOR_REGISTRY.items()
}
        exporters = []

        if self.settings.export_markdown:
            exporters.append(MarkdownExporter())

        if self.settings.export_docx:
            exporters.append(DocxExporter())

        exporters.append(MetadataExporter())

        self.export_manager = ExportManager(exporters=exporters)


    def finish(
        self,
        content: str,
        prefix: str,
        metadata: dict | None = None,
    ):
        print("\n")
        print(content)

        saved_paths = self.export_manager.save_all(
            content,
            prefix,
            metadata,
        )

        print("\nSaved files:")
        for path in saved_paths:
            print(f"- {path}")

            
    def build_title(self, values: dict) -> str:
        return (
            values.get("topic")
            or values.get("student_name")
            or values.get("situation")
            or "Untitled"
        )

def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===")

    for key, item in GENERATOR_REGISTRY.items():
        print(f"{key}. {item['name']}")

    print("6. View saved resources")

    choice = input("\nChoose: ").strip()

    if choice != "6" and choice not in GENERATOR_REGISTRY:
        print("Invalid option")
        return

    if choice == "6":
        resources = toolkit.library.all()

        print("\n=== Saved Resources ===\n")

        if not resources:
            print("No saved resources found.")
            return

        for index, resource in enumerate(resources, start=1):
            metadata = resource.get("metadata", {})

            resource_type = resource.get("type", "unknown")
            created_at = resource.get("created_at", "")
            grade = metadata.get("grade", "")
            topic = metadata.get("topic", "")
            student_name = metadata.get("student_name", "")
            situation = metadata.get("situation", "")


            title = metadata.get("title") or (
                topic
                or student_name
                or situation
                or "Untitled"
            )

            details = []

            if grade:
                details.append(f"Grade: {grade}")

            if metadata.get("curriculum"):
                details.append(f"Curriculum: {metadata.get('curriculum')}")

            detail_text = " | ".join(details)

            if detail_text:
                print(
                    f"{index}. {resource_type} | {title} | {detail_text} | {created_at}"
                )
            else:
                print(
                    f"{index}. {resource_type} | {title} | {created_at}"
                )

        return

    item = GENERATOR_REGISTRY[choice]
    values = {}

    for field, default in item["fields"].items():
        if default is None and field == "curriculum":
            default = toolkit.settings.default_curriculum

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

    metadata = {
        "title": toolkit.build_title(values),
        **values,
    }
    
    toolkit.finish(
        result,
        item["prefix"],
        metadata=metadata,
    )

if __name__ == "__main__":
    main()
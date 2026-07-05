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

    def create_quiz_from_lesson(self):
        lessons = self.library.find_by_type("lesson_plan")

        if not lessons:
            print("\nNo saved lessons found.")
            return

        print("\n=== Saved Lessons ===\n")

        for index, lesson in enumerate(lessons, start=1):
            metadata = lesson.get("metadata", {})
            title = metadata.get("title") or metadata.get("topic") or "Untitled"
            grade = metadata.get("grade", "")

            if grade:
                print(f"{index}. {title} | Grade: {grade}")
            else:
                print(f"{index}. {title}")

        choice = input("\nSelect lesson: ").strip()

        if not choice.isdigit():
            print("Invalid selection.")
            return

        selected_index = int(choice) - 1

        if selected_index < 0 or selected_index >= len(lessons):
            print("Invalid selection.")
            return

        lesson = lessons[selected_index]
        metadata = lesson.get("metadata", {})
        lesson_content = lesson.get("content", "")

        grade = metadata.get("grade", "2nd Grade")

        question_count = input("Question Count [10]: ").strip() or "10"

        print("\nGenerating quiz from saved lesson...\n")

        quiz_generator = self.generators["5"]

        result = quiz_generator.generate_from_lesson(
            lesson_content=lesson_content,
            grade=grade,
            question_count=question_count,
        )

        quiz_metadata = {
            "title": f"Quiz from {metadata.get('title') or metadata.get('topic') or 'Lesson'}",
            "source_lesson": metadata.get("title") or metadata.get("topic") or "Untitled",
            "grade": grade,
            "question_count": question_count,
            "relationships": {
                "created_from": lesson.get("id"),
                "created_from_type": lesson.get("type"),
            },
}

        self.finish(
            result,
            "quiz",
            metadata=quiz_metadata,
        )

    def create_worksheet_from_lesson(self):
        lessons = self.library.find_by_type("lesson_plan")

        if not lessons:
            print("\nNo saved lessons found.")
            return

        print("\n=== Saved Lessons ===\n")

        for index, lesson in enumerate(lessons, start=1):
            metadata = lesson.get("metadata", {})
            title = metadata.get("title") or metadata.get("topic") or "Untitled"
            grade = metadata.get("grade", "")

            if grade:
                print(f"{index}. {title} | Grade: {grade}")
            else:
                print(f"{index}. {title}")

        choice = input("\nSelect lesson: ").strip()

        if not choice.isdigit():
            print("Invalid selection.")
            return

        selected_index = int(choice) - 1

        if selected_index < 0 or selected_index >= len(lessons):
            print("Invalid selection.")
            return

        lesson = lessons[selected_index]
        metadata = lesson.get("metadata", {})
        lesson_content = lesson.get("content", "")
        grade = metadata.get("grade", "2nd Grade")

        print("\nGenerating worksheet from saved lesson...\n")

        worksheet_generator = self.generators["2"]

        result = worksheet_generator.generate_from_lesson(
            lesson_content=lesson_content,
            grade=grade,
        )

        worksheet_metadata = {
            "title": f"Worksheet from {metadata.get('title') or metadata.get('topic') or 'Lesson'}",
            "source_lesson": metadata.get("title") or metadata.get("topic") or "Untitled",
            "grade": grade,
            "relationships": {
                "created_from": lesson.get("id"),
                "created_from_type": lesson.get("type"),
        },
}

        self.finish(
            result,
            "worksheet",
            metadata=worksheet_metadata,
        )

def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===")

    for key, item in GENERATOR_REGISTRY.items():
        print(f"{key}. {item['name']}")

    print("6. View saved resources")
    print("7. Create quiz from saved lesson")
    print("8. Create worksheet from saved lesson")

    choice = input("\nChoose: ").strip()

    if choice not in ["6", "7", "8"] and choice not in GENERATOR_REGISTRY:
        print("Invalid option")
        return

    if choice == "6":
        query = input("Search saved resources, or press Enter for all: ").strip()
        resources = toolkit.library.search(query)

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

        open_choice = input(
            "\nOpen resource number, or press Enter to exit: "
        ).strip()

        if not open_choice:
            return

        if not open_choice.isdigit():
            print("Invalid selection.")
            return

        selected_index = int(open_choice) - 1

        if selected_index < 0 or selected_index >= len(resources):
            print("Invalid selection.")
            return

        selected_resource = resources[selected_index]

        print("\n=== Resource Content ===\n")
        print(selected_resource.get("content", ""))

        print("\nMetadata:")
        for key, value in selected_resource.get("metadata", {}).items():
            print(f"- {key}: {value}")

        return

    if choice == "7":
        toolkit.create_quiz_from_lesson()
        return

    if choice == "8":
        toolkit.create_worksheet_from_lesson()
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
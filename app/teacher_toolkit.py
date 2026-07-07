from sdk.ai import AI, AIConfig

from app.config.settings import Settings
from app.exporters.docx import DocxExporter
from app.exporters.manager import ExportManager
from app.exporters.markdown import MarkdownExporter
from app.exporters.metadata import MetadataExporter
from app.registry import GENERATOR_REGISTRY
from app.storage.library import ResourceLibrary
from app.users.manager import ProfileManager
from app.exporters.pdf import PdfExporter
from app.database.connection import Database
from app.repositories.teacher import TeacherRepository
from app.repositories.resource import ResourceRepository
from app.repositories.relationship import RelationshipRepository
from app.repositories.student import StudentRepository
from app.repositories.assessment import AssessmentRepository
from app.repositories.gradebook import GradebookRepository
from app.exporters.excel import ExcelGradebookExporter
from app.generators.intervention import InterventionGenerator
from app.generators.worksheet import WorksheetGenerator
from app.generators.quiz import QuizGenerator
from app.modules.gradebook import GradebookModule
from app.modules.students import StudentModule
from app.modules.profiles import ProfileModule
from app.modules.resources import ResourceModule


class TeacherToolkit:
    def __init__(self):
        self.settings = Settings()
        self.library = ResourceLibrary()
        self.profile_manager = ProfileManager()

        try:
            self.teacher_profile = self.profile_manager.get_active()

            if self.teacher_profile is None:
                profiles = self.profile_manager.list_profiles()

                if profiles:
                    first = profiles[0]["file"]
                    self.profile_manager.set_active(first)
                    self.teacher_profile = self.profile_manager.load(first)

            if self.teacher_profile:
                print()
                print(f"Welcome {self.teacher_profile.name}")
                print(f"School: {self.teacher_profile.school}")

            else:
                self.teacher_profile = self.settings
                print()
                print("No teacher profile found.")
                print("Using default settings.")

        except FileNotFoundError:
            self.teacher_profile = self.settings
            print()
            print("No teacher profile found.")
            print("Using default settings.")
        
        self.database = Database()
        self.database.initialize()

        self.teacher_repository = TeacherRepository(self.database)
        self.resource_repository = ResourceRepository(self.database)
        self.student_repository = StudentRepository(self.database)
        self.assessment_repository = AssessmentRepository(self.database)
        self.gradebook_repository = GradebookRepository(self.database)
        self.excel_exporter = ExcelGradebookExporter()
        self.gradebook_module = GradebookModule(self)
        self.student_module = StudentModule(self)
        self.profile_module = ProfileModule(self)
        self.resource_module = ProfileModule(self)
        self.resource_module = ResourceModule(self)
        self.relationship_repository = RelationshipRepository(
            self.database
        )

        self.teacher_id = None

        if hasattr(self.teacher_profile, "name"):
            self.teacher_id = self.teacher_repository.save(
                self.teacher_profile
            )
        
        self.ai = AI(
            AIConfig(
                provider=self.settings.ai_provider,
                model=self.settings.ai_model,
            )
        )
        self.intervention_generator = InterventionGenerator(
            self.ai,
            self.teacher_profile,
        )

        self.worksheet_generator = WorksheetGenerator(
            self.ai,
            self.teacher_profile,
        )

        self.quiz_generator = QuizGenerator(
            self.ai,
            self.teacher_profile,
        )

        self.generators = {
            key: item["class"](
                self.ai,
                self.teacher_profile,
            )
            for key, item in GENERATOR_REGISTRY.items()
        }

        exporters = []

        if self.settings.export_markdown:
            exporters.append(MarkdownExporter())

        if self.settings.export_docx:
            exporters.append(DocxExporter())

        if getattr(self.settings, "export_pdf", False):
            exporters.append(PdfExporter())

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

        if self.teacher_id:
            title = "Untitled"

            if metadata:
                title = metadata.get("title", title)

            resource_id = self.resource_repository.save(
                teacher_id=self.teacher_id,
                resource_type=prefix,
                title=title,
                content=content,
            )

            print(f"- database resource id: {resource_id}")
            return resource_id

    def build_title(self, values: dict) -> str:
        return (
            values.get("topic")
            or values.get("student_name")
            or values.get("situation")
            or "Untitled"
        )



    def _select_assessment(self):
        assessments = self.assessment_repository.list_by_teacher(
            self.teacher_id
        )

        if not assessments:
            print("\nNo assessments found.")
            return None

        print("\n=== Assessments ===\n")

        for index, assessment in enumerate(assessments, start=1):
            print(
                f"{index}. {assessment['title']} | {assessment['assessment_type']} | Max: {assessment['max_score']}"
            )

        selected = input("\nChoose assessment: ").strip()

        if not selected.isdigit():
            print("Invalid option.")
            return None

        index = int(selected) - 1

        if index < 0 or index >= len(assessments):
            print("Invalid option.")
            return None

        return assessments[index]


def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===")

    for key, item in GENERATOR_REGISTRY.items():
        print(f"{key}. {item['name']}")

    print("6. View saved resources")
    print("7. Create quiz from saved lesson")
    print("8. Create worksheet from saved lesson")
    print("9. View lesson resources")
    print("10. Teacher profiles")
    print("11. Manage students")
    print("12. Gradebook")

    choice = input("\nChoose: ").strip()

    if choice not in ["6", "7", "8", "9", "10", "11", "12"] and choice not in GENERATOR_REGISTRY:
        print("Invalid option")
        return

    if choice == "6":
        toolkit.resource_module.view_saved_resources()
        return

    if choice == "7":
        toolkit.resource_module.create_quiz_from_lesson()
        return

    if choice == "8":
        toolkit.resource_module.create_worksheet_from_lesson()
        return

    if choice == "9":
        toolkit.resource_module.view_lesson_resources()
        return

    if choice == "10":
        toolkit.profile_module.run()
        return

    if choice == "11":
        toolkit.student_module.run()
        return

    if choice == "12":
        toolkit.gradebook_module.run()
        return

        item = GENERATOR_REGISTRY[choice]
    values = {}

    profile = toolkit.teacher_profile

    item = GENERATOR_REGISTRY[choice]
    values = {}

    #print("DEBUG choice:", choice)
    #print("DEBUG item:", item)

    for field, default in item["fields"].items():

        # curriculum from profile
        if field == "curriculum":
            profile_curriculum = getattr(
                profile,
                "curriculum",
                None,
            )

            if profile_curriculum:
                values[field] = profile_curriculum
                continue

            default = toolkit.settings.default_curriculum

        # grade from profile
        if field == "grade":
            profile_grades = getattr(
                profile,
                "grades",
                None,
            )

            if profile_grades:
                default = profile_grades[0]

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
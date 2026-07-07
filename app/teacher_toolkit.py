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

    def create_quiz_from_lesson(self):
        lessons = self.resource_repository.find_by_type(
            "lesson_plan"
        )

        if not lessons:
            print("\nNo saved lessons found.")
            return

        print("\n=== Saved Lessons ===\n")

        for index, lesson in enumerate(lessons, start=1):
            metadata = {
                "title": lesson.get("title"),
            }
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
        metadata = {
            "title": lesson.get("title"),
        }
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

        quiz_id = self.finish(
            result,
            "quiz",
            metadata,
        )

        if quiz_id:
            self.relationship_repository.save(
                source_id=lesson["id"],
                target_id=quiz_id,
                relationship_type="quiz",
            )



    def create_worksheet_from_lesson(self):
        lessons = self.resource_repository.find_by_type(
            "lesson_plan"
        )

        if not lessons:
            print("\nNo saved lessons found.")
            return

        print("\n=== Saved Lessons ===\n")

        for index, lesson in enumerate(lessons, start=1):
            metadata = {
                "title": lesson.get("title"),
            }
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
        metadata = {
            "title": lesson.get("title"),
        }
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

        worksheet_id = self.finish(
            result,
            "worksheet",
            metadata,
        )

        if worksheet_id:
            self.relationship_repository.save(
                source_id=lesson["id"],
                target_id=worksheet_id,
                relationship_type="worksheet",
            )
        
    def manage_profiles(self):
        print("\n=== Teacher Profiles ===\n")
        print("1. View current profile")
        print("2. Create new profile")
        print("3. Edit current profile")
        print("4. Switch profile")
        print("5. List profiles")

        choice = input("\nChoose: ").strip()

        # VIEW CURRENT
        if choice == "1":
            profile = self.teacher_profile

            grades = getattr(profile, "grades", []) or []
            subjects = getattr(profile, "subjects", []) or []

            print("\n=== Current Profile ===\n")
            print(f"Name: {getattr(profile, 'name', '')}")
            print(f"School: {getattr(profile, 'school', '')}")
            print(f"Grades: {', '.join(grades)}")
            print(f"Subjects: {', '.join(subjects)}")
            print(f"Curriculum: {getattr(profile, 'curriculum', '')}")
            print(f"Teaching Style: {getattr(profile, 'teaching_style', '')}")
            return

        # CREATE OR EDIT
        if choice in ["2", "3"]:
            from app.users.profile import TeacherProfile

            current = None

            if choice == "3":
                current = self.teacher_profile

            print("\n=== Teacher Profile ===\n")

            current_name = getattr(current, "name", "") if current else ""
            current_school = getattr(current, "school", "") if current else ""
            current_grades = ", ".join(getattr(current, "grades", []) or []) if current else ""
            current_subjects = ", ".join(getattr(current, "subjects", []) or []) if current else ""
            current_curriculum = getattr(current, "curriculum", "") if current else ""
            current_style = getattr(current, "teaching_style", "") if current else ""

            name = input(f"Teacher Name [{current_name}]: ").strip() or current_name
            school = input(f"School [{current_school}]: ").strip() or current_school
            grades = input(f"Grades [{current_grades}]: ").strip() or current_grades
            subjects = input(f"Subjects [{current_subjects}]: ").strip() or current_subjects
            curriculum = input(f"Curriculum [{current_curriculum}]: ").strip() or current_curriculum
            style = input(f"Teaching Style [{current_style}]: ").strip() or current_style

            profile = TeacherProfile(
                name=name,
                school=school,
                grades=[
                    x.strip()
                    for x in grades.split(",")
                    if x.strip()
                ],
                subjects=[
                    x.strip()
                    for x in subjects.split(",")
                    if x.strip()
                ],
                curriculum=curriculum,
                teaching_style=style,
            )

            path = self.profile_manager.save(profile)

            self.profile_manager.set_active(
                path.stem
            )

            self.teacher_profile = profile

            print(f"\nSaved: {path}")
            print("Profile is now active.")
            return

        # SWITCH
        if choice == "4":
            profiles = self.profile_manager.list_profiles()

            print("\n=== Available Profiles ===\n")

            for index, profile in enumerate(profiles, start=1):
                print(
                    f"{index}. {profile['name']}"
                )

            selected = input("\nChoose profile: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(profiles):
                print("Invalid option.")
                return

            selected_profile = profiles[index]

            self.profile_manager.set_active(
                selected_profile["file"]
            )

            self.teacher_profile = (
                self.profile_manager.get_active()
            )

            print(
                f"\nSwitched to {self.teacher_profile.name}"
            )

            return

        # LIST
        if choice == "5":
            profiles = self.profile_manager.list_profiles()

            print("\n=== Profiles ===\n")

            for profile in profiles:
                print(f"- {profile['name']}")

            return

        print("Invalid option.")
        
    def view_lesson_resources(self):
        lessons = self.resource_repository.find_by_type(
            "lesson_plan"
        )

        if not lessons:
            print("\nNo saved lessons found.")
            return

        print("\n=== Saved Lessons ===\n")

        for index, lesson in enumerate(lessons, start=1):
            title = (
                lesson.get("title")
                or lesson.get("metadata", {}).get("title")
                or "Untitled"
            )
            grade = lesson.get("metadata", {}).get("grade", "")

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
        related = self.library.find_related_to(lesson.get("id"))

        print("\n=== Related Resources ===\n")

        if not related:
            print("No related resources found.")
            return

        for index, resource in enumerate(related, start=1):
            title = (
                resource.get("title")
                or resource.get("metadata", {}).get("title")
                or "Untitled"
            )
            resource_type = resource.get("type", "unknown")
            created_at = resource.get("created_at", "")

            print(f"{index}. {resource_type} | {title} | {created_at}")

    def manage_students(self):
        print("\n=== Students ===\n")
        print("1. List students")
        print("2. Add student")
        print("3. Import students from file (future)")
        print("4. View student performance (future)")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            students = self.student_repository.list_by_teacher(
                self.teacher_id
            )

            print("\n=== Student List ===\n")

            if not students:
                print("No students found.")
                return

            for index, student in enumerate(students, start=1):
                name = f"{student.get('first_name', '')} {student.get('last_name', '')}".strip()
                grade = student.get("grade_level", "")

                if grade:
                    print(f"{index}. {name} | Grade: {grade}")
                else:
                    print(f"{index}. {name}")

            return

        if choice == "2":
            print("\n=== Add Student ===\n")

            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            grade_level = input("Grade level: ").strip()

            if not first_name:
                print("First name is required.")
                return

            student_id = self.student_repository.save(
                teacher_id=self.teacher_id,
                first_name=first_name,
                last_name=last_name,
                grade_level=grade_level,
            )

            print(f"\nStudent saved with ID: {student_id}")
            return

        if choice in ["3", "4"]:
            print("\nComing soon.")
            return

        print("Invalid option.")

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
        query = input("Search saved resources, or press Enter for all: ").strip()
        #resources = toolkit.library.search(query)
        resources = toolkit.resource_repository.search(query)

        print("\n=== Saved Resources ===\n")

        if not resources:
            print("No saved resources found.")
            return

        for index, resource in enumerate(resources, start=1):
            metadata = resource.get("metadata", {})

            resource_type = resource.get("type", "unknown")
            created_at = resource.get("created_at", "")
            title = resource.get("title") or "Untitled"

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

        print("\nDatabase Info:")
        print(f"- ID: {selected_resource.get('id')}")
        print(f"- Teacher ID: {selected_resource.get('teacher_id')}")
        print(f"- Type: {selected_resource.get('type')}")
        print(f"- Created At: {selected_resource.get('created_at')}")

        return

    if choice == "7":
        toolkit.create_quiz_from_lesson()
        return

    if choice == "8":
        toolkit.create_worksheet_from_lesson()
        return

    if choice == "9":
        toolkit.view_lesson_resources()
        return

    if choice == "10":
        toolkit.manage_profiles()
        return

    if choice == "11":
        toolkit.manage_students()
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
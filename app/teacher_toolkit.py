from sdk.ai import AI, AIConfig

from app.generators.lesson import LessonGenerator
from app.generators.worksheet import WorksheetGenerator
from app.generators.parent_email import ParentEmailGenerator

from app.exporters.markdown import MarkdownExporter
from app.exporters.docx import DocxExporter


class TeacherToolkit:
    def __init__(self):
        self.ai = AI(
            AIConfig(
                provider="ollama",
                model="qwen3:32b",
            )
        )

        self.lessons = LessonGenerator(self.ai)
        self.worksheets = WorksheetGenerator(self.ai)
        self.parent_emails = ParentEmailGenerator(self.ai)

        self.markdown_exporter = MarkdownExporter()
        self.docx_exporter = DocxExporter()

    def create_lesson(self):
        grade = input("Grade: ").strip()
        topic = input("Topic: ").strip()

        result = self.lessons.generate(
            topic=topic,
            grade=grade,
        )

        self.finish(
            result,
            "lesson_plan",
        )

    def create_worksheet(self):
        grade = input("Grade: ").strip()
        topic = input("Topic: ").strip()

        result = self.worksheets.generate(
            topic=topic,
            grade=grade,
        )

        self.finish(
            result,
            "worksheet",
        )

    def create_parent_email(self):
        situation = input(
            "Describe situation: "
        ).strip()

        result = self.parent_emails.generate(
            situation=situation,
        )

        self.finish(
            result,
            "parent_email",
        )

    def finish(
        self,
        content: str,
        prefix: str,
    ):
        print("\n")
        print(content)

        md_path = self.markdown_exporter.save(
            content,
            prefix,
        )

        docx_path = self.docx_exporter.save(
            content,
            prefix,
        )

        print(f"\nSaved Markdown: {md_path}")
        print(f"Saved DOCX: {docx_path}")

def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===")
    print("1. Lesson plan")
    print("2. Worksheet")
    print("3. Parent email")

    choice = input("\nChoose: ").strip()

    if choice == "1":
        toolkit.create_lesson()

    elif choice == "2":
        toolkit.create_worksheet()

    elif choice == "3":
        toolkit.create_parent_email()

    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
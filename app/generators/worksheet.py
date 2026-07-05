from app.templates.loader import TemplateLoader


class WorksheetGenerator:
    def __init__(self, ai, settings=None):
        self.ai = ai
        self.settings = settings
        self.templates = TemplateLoader()

    def generate(self, topic: str, grade: str, curriculum: str) -> str:
        prompt = self.templates.render(
            "worksheet.txt",
            {
                "grade": grade,
                "topic": topic,
                "curriculum": curriculum,
                "school": self.settings.school if self.settings else "",
                "teaching_style": self.settings.teaching_style if self.settings else "",
            },
        )

    def generate_from_lesson(
        self,
        lesson_content: str,
        grade: str = "2nd Grade",
    ) -> str:
        prompt = f"""
        You are an expert elementary teacher.

        Create a printable worksheet based on the lesson below.

        Grade: {grade}

        Lesson:
        {lesson_content}

        Include:
        - student name line
        - date line
        - clear directions
        - 10 practice problems
        - 2 challenge problems
        - answer key
        """

        return self.ai.chat(prompt)

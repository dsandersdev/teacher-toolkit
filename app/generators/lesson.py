from app.templates.loader import TemplateLoader


class LessonGenerator:
    def __init__(self, ai, settings=None):
        self.ai = ai
        self.settings = settings
        self.templates = TemplateLoader()
    def generate(self, topic: str, grade: str, curriculum: str) -> str:
        prompt = self.templates.render(
            "lesson.txt",
            {
                "grade": grade,
                "topic": topic,
                "curriculum": curriculum,
                "school": self.settings.school if self.settings else "",
                "teaching_style": self.settings.teaching_style if self.settings else "",
            },
        )

        return self.ai.chat(prompt)
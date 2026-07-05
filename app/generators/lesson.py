from app.templates.loader import TemplateLoader


class LessonGenerator:
    def __init__(self, ai):
        self.ai = ai
        self.templates = TemplateLoader()

    def generate(self, topic: str, grade: str) -> str:
        prompt = self.templates.render(
            "lesson.txt",
            {
                "grade": grade,
                "topic": topic,
            },
        )

        return self.ai.chat(prompt)
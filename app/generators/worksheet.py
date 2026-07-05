from app.templates.loader import TemplateLoader


class WorksheetGenerator:
    def __init__(self, ai):
        self.ai = ai
        self.templates = TemplateLoader()

    def generate(self, topic: str, grade: str, curriculum: str) -> str:
        prompt = self.templates.render(
            "worksheet.txt",
            {
                "grade": grade,
                "topic": topic,
                "curriculum": curriculum,
            },
        )

        return self.ai.chat(prompt)
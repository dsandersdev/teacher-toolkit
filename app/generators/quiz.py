from app.templates.loader import TemplateLoader


class QuizGenerator:
    def __init__(self, ai, settings=None):
        self.ai = ai
        self.settings = settings
        self.templates = TemplateLoader()

    def generate(
        self,
        grade: str,
        topic: str,
        curriculum: str = "",
        question_count: str = "10",
    ) -> str:
        prompt = self.templates.render(
            "quiz.txt",
            {
                "grade": grade,
                "topic": topic,
                "curriculum": curriculum,
                "question_count": question_count,
                "school": self.settings.school if self.settings else "",
                "teaching_style": self.settings.teaching_style if self.settings else "",
            },
        )

        return self.ai.chat(prompt)
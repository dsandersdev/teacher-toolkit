from app.templates.loader import TemplateLoader


class ReportCommentGenerator:
    def __init__(self, ai):
        self.ai = ai
        self.templates = TemplateLoader()

    def generate(
        self,
        student_name: str,
        strengths: str,
        growth: str,
        tone: str = "professional, supportive, and encouraging",
    ) -> str:
        prompt = self.templates.render(
            "report_comment.txt",
            {
                "student_name": student_name,
                "strengths": strengths,
                "growth": growth,
                "tone": tone,
            },
        )

        return self.ai.chat(prompt)
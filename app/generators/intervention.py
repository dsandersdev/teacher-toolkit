from app.templates.loader import TemplateLoader


class InterventionGenerator:
    def __init__(self, ai, settings=None):
        self.ai = ai
        self.settings = settings
        self.templates = TemplateLoader()

    def generate(
        self,
        assessment_title: str,
        students: str,
        grade: str = "",
    ) -> str:
        prompt = self.templates.render(
            "intervention.txt",
            {
                "assessment_title": assessment_title,
                "students": students,
                "grade": grade,
                "school": self.settings.school if self.settings else "",
                "teaching_style": self.settings.teaching_style if self.settings else "",
            },
        )

        return self.ai.chat(prompt)
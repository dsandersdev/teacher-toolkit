from app.templates.loader import TemplateLoader


class ParentEmailGenerator:
    def __init__(self, ai, settings:None):
        self.ai = ai
        self.settings = settings
        self.templates = TemplateLoader()

    def generate(
        self,
        situation: str,
        tone: str = "friendly and professional",
    ) -> str:
        prompt = self.templates.render(
            "parent_email.txt",
            {
                "situation": situation,
                "tone": tone,
            },
        )

        return self.ai.chat(prompt)
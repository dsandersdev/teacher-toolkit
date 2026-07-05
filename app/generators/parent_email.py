class ParentEmailGenerator:
    def __init__(self, ai):
        self.ai = ai

    def generate(
        self,
        situation: str,
        tone: str = "friendly and professional",
    ) -> str:
        prompt = f"""
        You are an experienced teacher.

        Write a parent communication email.

        Situation:
        {situation}

        Requirements:
        - Tone: {tone}
        - Warm greeting
        - Clear explanation
        - Supportive language
        - Professional closing
        """

        return self.ai.chat(prompt)
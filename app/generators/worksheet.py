class WorksheetGenerator:
    def __init__(self, ai):
        self.ai = ai

    def generate(self, topic: str, grade: str) -> str:
        prompt = f"""
        You are an expert elementary teacher.

        Create a printable worksheet.

        Grade: {grade}
        Topic: {topic}

        Include:
        - student name line
        - date line
        - directions
        - 10 practice problems
        - 2 challenge problems
        - answer key
        """

        return self.ai.chat(prompt)
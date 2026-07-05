class ReportCommentGenerator:
    def __init__(self, ai):
        self.ai = ai

    def generate(
        self,
        student_name: str,
        strengths: str,
        growth: str,
        tone: str = "professional, supportive, and encouraging",
    ) -> str:

        prompt = f"""
        You are an experienced elementary teacher.

        Write a personalized report card comment.

        Student:
        {student_name}

        Strengths:
        {strengths}

        Areas for growth:
        {growth}

        Requirements:
        - Tone: {tone}
        - Start positively
        - Mention specific strengths
        - Address growth areas constructively
        - Include encouragement for continued progress
        - Sound natural and teacher-written
        """

        return self.ai.chat(prompt)
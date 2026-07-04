from sdk.ai import AIConfig, AI


class TeacherToolkit:
    """
    AI powered teacher assistant.

    Features planned:
    - Lesson generation
    - Worksheets
    - Parent communication
    - Rubrics
    - Assessments
    """

    def __init__(self):
        self.ai = AI(
            AIConfig(
                provider="ollama",
                model="qwen3:32b"
            )
        )

    def generate_lesson(self, topic: str, grade: str):
        prompt = f"""
        You are an expert teacher.

        Create a complete lesson plan.

        Grade: {grade}
        Topic: {topic}

        Include:
        - Learning objectives
        - Standards
        - Materials
        - Warm-up
        - Direct instruction
        - Guided practice
        - Independent practice
        - Differentiation
        - Assessment
        """

        return self.ai.chat(prompt)


if __name__ == "__main__":
    toolkit = TeacherToolkit()

    result = toolkit.generate_lesson(
        topic="Addition and subtraction within 100",
        grade="2nd Grade",
    )

    print(result)
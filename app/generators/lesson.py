class LessonGenerator:
    def __init__(self, ai):
        self.ai = ai
        
    def generator(self, topic: str, grade: str) -> str:
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
            - Direct instruction
            - Guided practice
            - Independent practice
            - Differentiation
            - Assessment
            """

        return self.ai.chat(prompt)
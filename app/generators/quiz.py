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

    def generate_from_lesson(
        self,
        lesson_content: str,
        grade: str = "2nd Grade",
        question_count: str = "10",
    ) -> str:
        prompt = f"""
        You are an expert elementary teacher.

        Create a quiz based on the lesson below.

        Grade: {grade}
        Number of questions: {question_count}

        Lesson:
        {lesson_content}

        Include:
        - student name line
        - date line
        - clear directions
        - a mix of question types
        - answer key
        - optional challenge question
        """

        return self.ai.chat(prompt)
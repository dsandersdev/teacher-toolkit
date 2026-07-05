from app.generators.lesson import LessonGenerator
from app.generators.quiz import QuizGenerator
from app.generators.worksheet import WorksheetGenerator


class FakeAI:
    def chat(self, prompt: str) -> str:
        return "Generated test content"


def test_lesson_generator_returns_content():
    generator = LessonGenerator(ai=FakeAI())

    content = generator.generate(
        topic="Addition within 20",
        grade="2",
        curriculum="General",
    )

    assert isinstance(content, str)
    assert len(content.strip()) > 0


def test_quiz_generator_returns_content():
    generator = QuizGenerator(ai=FakeAI())

    content = generator.generate(
        topic="Addition within 20",
        grade="2",
        curriculum="General",
        question_count="5",
    )

    assert isinstance(content, str)
    assert len(content.strip()) > 0


def test_worksheet_generator_returns_content():
    generator = WorksheetGenerator(ai=FakeAI())

    content = generator.generate(
        topic="Addition within 20",
        grade="2",
        curriculum="General",
    )

    assert isinstance(content, str)
    assert len(content.strip()) > 0
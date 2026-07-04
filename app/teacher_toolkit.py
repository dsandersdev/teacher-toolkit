from datetime import datetime
from pathlib import Path

from sdk.ai import AIConfig, AI


class TeacherToolkit:
    def __init__(self):
        self.ai = AI(
            AIConfig(
                provider="ollama",
                model="qwen3:32b",
            )
        )

        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)

    def generate_lesson(self, topic: str, grade: str) -> str:
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

    def save_output(self, content: str, prefix: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.md"
        output_path = self.output_dir / filename

        output_path.write_text(content, encoding="utf-8")
        return output_path


def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===\n")

    grade = input("Grade: ").strip()
    topic = input("Lesson topic: ").strip()

    if not grade:
        grade = "2nd Grade"

    if not topic:
        topic = "Addition and subtraction within 100"

    print("\nGenerating lesson plan...\n")

    lesson = toolkit.generate_lesson(topic=topic, grade=grade)

    print("\n=== Generated Lesson Plan ===\n")
    print(lesson)

    saved_path = toolkit.save_output(lesson, "lesson_plan")

    print(f"\nSaved to: {saved_path}")


if __name__ == "__main__":
    main()
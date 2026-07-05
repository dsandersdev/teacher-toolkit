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

    def generate_worksheet(self, topic: str, grade: str) -> str:
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

    def generate_parent_email(
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


    def save_output(self, content: str, prefix: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.md"
        output_path = self.output_dir / filename

        output_path.write_text(content, encoding="utf-8")
        return output_path


def main():
    toolkit = TeacherToolkit()

    print("\n=== Teacher Toolkit ===\n")
    print("1. Lesson plan")
    print("2. Worksheet")
    print("3. Parent email")

    choice = input("\nChoose an option: ").strip()

    if choice in ["1", "2"]:
        grade = input("Grade: ").strip()
        topic = input("Topic: ").strip()

        if not grade:
            grade = "2nd Grade"

        if not topic:
            topic = "Addition and subtraction within 100"

        if choice == "2":
            print("\nGenerating worksheet...\n")

            result = toolkit.generate_worksheet(
                topic=topic,
                grade=grade,
            )

            prefix = "worksheet"
            title = "Generated Worksheet"

        else:
            print("\nGenerating lesson plan...\n")

            result = toolkit.generate_lesson(
                topic=topic,
                grade=grade,
            )

            prefix = "lesson_plan"
            title = "Generated Lesson Plan"

    elif choice == "3":
        situation = input("Describe situation: ").strip()

        print("\nGenerating parent email...\n")

        result = toolkit.generate_parent_email(
            situation=situation
        )

        prefix = "parent_email"
        title = "Generated Parent Email"

    else:
        print("Invalid option.")
        return

    print(f"\n=== {title} ===\n")
    print(result)

    saved_path = toolkit.save_output(
        result,
        prefix,
    )

    print(f"\nSaved to: {saved_path}")

if __name__ == "__main__":
    main()
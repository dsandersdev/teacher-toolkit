class ResourceModule:
    def __init__(self, toolkit):
        self.toolkit = toolkit

    def view_saved_resources(self):
        query = input("Search saved resources, or press Enter for all: ").strip()
        resources = self.toolkit.resource_repository.search(query)

        print("\n=== Saved Resources ===\n")

        if not resources:
            print("No saved resources found.")
            return

        for index, resource in enumerate(resources, start=1):
            resource_type = resource.get("type", "unknown")
            created_at = resource.get("created_at", "")
            title = resource.get("title") or "Untitled"

            print(
                f"{index}. {resource_type} | {title} | {created_at}"
            )

        open_choice = input(
            "\nOpen resource number, or press Enter to exit: "
        ).strip()

        if not open_choice:
            return

        if not open_choice.isdigit():
            print("Invalid selection.")
            return

        selected_index = int(open_choice) - 1

        if selected_index < 0 or selected_index >= len(resources):
            print("Invalid selection.")
            return

        selected_resource = resources[selected_index]

        print("\n=== Resource Content ===\n")
        print(selected_resource.get("content", ""))

        print("\nDatabase Info:")
        print(f"- ID: {selected_resource.get('id')}")
        print(f"- Teacher ID: {selected_resource.get('teacher_id')}")
        print(f"- Type: {selected_resource.get('type')}")
        print(f"- Created At: {selected_resource.get('created_at')}")
    
    def create_quiz_from_lesson(self):
        lessons = self.toolkit.resource_repository.search("lesson_plan")

        print("\n=== Saved Lessons ===\n")

        if not lessons:
            print("No saved lessons found.")
            return

        for index, lesson in enumerate(lessons, start=1):
            print(
                f"{index}. {lesson.get('title')}"
            )

        choice = input(
            "\nChoose lesson: "
        ).strip()

        if not choice.isdigit():
            print("Invalid choice.")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(lessons):
            print("Invalid choice.")
            return

        lesson = lessons[index]

        print("\nGenerating quiz...\n")

        result = self.toolkit.quiz_generator.generate(
            topic=lesson.get("title"),
            grade="",
            curriculum=lesson.get("content"),
        )

        metadata = {
            "title": (
                f"Quiz from "
                f"{lesson.get('title')}"
            ),
            "source_resource": lesson.get("id"),
        }

        self.toolkit.finish(
            result,
            "quiz",
            metadata=metadata,
        )

    def create_worksheet_from_lesson(self):
        lessons = self.toolkit.resource_repository.search("lesson_plan")

        print("\n=== Saved Lessons ===\n")

        if not lessons:
            print("No saved lessons found.")
            return

        for index, lesson in enumerate(lessons, start=1):
            print(
                f"{index}. {lesson.get('title')}"
            )

        choice = input("\nChoose lesson: ").strip()

        if not choice.isdigit():
            print("Invalid choice.")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(lessons):
            print("Invalid choice.")
            return

        lesson = lessons[index]

        print("\nGenerating worksheet...\n")

        result = self.toolkit.worksheet_generator.generate(
            topic=lesson.get("title"),
            grade="",
            curriculum=lesson.get("content"),
        )

        metadata = {
            "title": (
                f"Worksheet from "
                f"{lesson.get('title')}"
            ),
            "source_resource": lesson.get("id"),
        }

        self.toolkit.finish(
            result,
            "worksheet",
            metadata=metadata,
        )

    def view_lesson_resources(self):
        lessons = self.toolkit.resource_repository.search("lesson_plan")

        print("\n=== Lesson Resources ===\n")

        if not lessons:
            print("No saved lesson resources found.")
            return

        for index, lesson in enumerate(lessons, start=1):
            print(
                f"{index}. {lesson.get('title')} | {lesson.get('created_at')}"
            )

        choice = input(
            "\nOpen lesson number, or press Enter to exit: "
        ).strip()

        if not choice:
            return

        if not choice.isdigit():
            print("Invalid choice.")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(lessons):
            print("Invalid choice.")
            return

        lesson = lessons[index]

        print("\n=== Lesson ===\n")
        print(lesson.get("content", ""))

        print("\nLesson Info:")
        print(f"- ID: {lesson.get('id')}")
        print(f"- Title: {lesson.get('title')}")
        print(f"- Created At: {lesson.get('created_at')}")
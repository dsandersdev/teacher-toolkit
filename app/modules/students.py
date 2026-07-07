class StudentModule:
    def __init__(self, toolkit):
        self.toolkit = toolkit

    def run(self):
        return self.manage_students()

    def manage_students(self):
        print("\n=== Students ===\n")
        print("1. List students")
        print("2. Add student")
        print("3. Import students from file (future)")
        print("4. View student performance (future)")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            students = self.toolkit.student_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            print("\n=== Student List ===\n")

            if not students:
                print("No students found.")
                return

            for index, student in enumerate(students, start=1):
                name = f"{student.get('first_name', '')} {student.get('last_name', '')}".strip()
                grade = student.get("grade_level", "")

                if grade:
                    print(f"{index}. {name} | Grade: {grade}")
                else:
                    print(f"{index}. {name}")

            return

        if choice == "2":
            print("\n=== Add Student ===\n")

            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            grade_level = input("Grade level: ").strip()

            if not first_name:
                print("First name is required.")
                return

            student_id = self.toolkit.student_repository.save(
                teacher_id=self.toolkit.teacher_id,
                first_name=first_name,
                last_name=last_name,
                grade_level=grade_level,
            )

            print(f"\nStudent saved with ID: {student_id}")
            return

        if choice in ["3", "4"]:
            print("\nComing soon.")
            return

        print("Invalid option.")


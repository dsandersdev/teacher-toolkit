class ProfileModule:
    def __init__(self, toolkit):
        self.toolkit = toolkit

    def run(self):
        return self.manage_profiles()

    def manage_profiles(self):
        print("\n=== Teacher Profiles ===\n")
        print("1. View current profile")
        print("2. Create new profile")
        print("3. Edit current profile")
        print("4. Switch profile")
        print("5. List profiles")

        choice = input("\nChoose: ").strip()

        # VIEW CURRENT
        if choice == "1":
            profile = self.toolkit.teacher_profile

            grades = getattr(profile, "grades", []) or []
            subjects = getattr(profile, "subjects", []) or []

            print("\n=== Current Profile ===\n")
            print(f"Name: {getattr(profile, 'name', '')}")
            print(f"School: {getattr(profile, 'school', '')}")
            print(f"Grades: {', '.join(grades)}")
            print(f"Subjects: {', '.join(subjects)}")
            print(f"Curriculum: {getattr(profile, 'curriculum', '')}")
            print(f"Teaching Style: {getattr(profile, 'teaching_style', '')}")
            return

        # CREATE OR EDIT
        if choice in ["2", "3"]:
            from app.users.profile import TeacherProfile

            current = None

            if choice == "3":
                current = self.toolkit.teacher_profile

            print("\n=== Teacher Profile ===\n")

            current_name = getattr(current, "name", "") if current else ""
            current_school = getattr(current, "school", "") if current else ""
            current_grades = ", ".join(getattr(current, "grades", []) or []) if current else ""
            current_subjects = ", ".join(getattr(current, "subjects", []) or []) if current else ""
            current_curriculum = getattr(current, "curriculum", "") if current else ""
            current_style = getattr(current, "teaching_style", "") if current else ""

            name = input(f"Teacher Name [{current_name}]: ").strip() or current_name
            school = input(f"School [{current_school}]: ").strip() or current_school
            grades = input(f"Grades [{current_grades}]: ").strip() or current_grades
            subjects = input(f"Subjects [{current_subjects}]: ").strip() or current_subjects
            curriculum = input(f"Curriculum [{current_curriculum}]: ").strip() or current_curriculum
            style = input(f"Teaching Style [{current_style}]: ").strip() or current_style

            profile = TeacherProfile(
                name=name,
                school=school,
                grades=[
                    x.strip()
                    for x in grades.split(",")
                    if x.strip()
                ],
                subjects=[
                    x.strip()
                    for x in subjects.split(",")
                    if x.strip()
                ],
                curriculum=curriculum,
                teaching_style=style,
            )

            path = self.toolkit.profile_manager.save(profile)

            self.toolkit.profile_manager.set_active(
                path.stem
            )

            self.toolkit.teacher_profile = profile

            print(f"\nSaved: {path}")
            print("Profile is now active.")
            return

        # SWITCH
        if choice == "4":
            profiles = self.toolkit.profile_manager.list_profiles()

            print("\n=== Available Profiles ===\n")

            for index, profile in enumerate(profiles, start=1):
                print(
                    f"{index}. {profile['name']}"
                )

            selected = input("\nChoose profile: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(profiles):
                print("Invalid option.")
                return

            selected_profile = profiles[index]

            self.toolkit.profile_manager.set_active(
                selected_profile["file"]
            )

            self.toolkit.teacher_profile = (
                self.toolkit.profile_manager.get_active()
            )

            print(
                f"\nSwitched to {self.toolkit.teacher_profile.name}"
            )

            return

        # LIST
        if choice == "5":
            profiles = self.toolkit.profile_manager.list_profiles()

            print("\n=== Profiles ===\n")

            for profile in profiles:
                print(f"- {profile['name']}")

            return

        print("Invalid option.")

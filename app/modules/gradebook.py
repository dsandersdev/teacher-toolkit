class GradebookModule:
    def __init__(self, toolkit):
        self.toolkit = toolkit

    def run(self):
        return self.manage_gradebook()

        
    def manage_gradebook(self):
        print("\n=== Gradebook ===\n")
        print("1. Create assessment")
        print("2. Enter student scores")
        print("3. View assessment results")
        print("4. Find students needing support")
        print("5. Export Excel")
        print("6. Generate AI intervention plan")
        print("7. Create worksheet from intervention plan")
        print("8. Create quiz from intervention plan")
        print("9. View student progress tracker")
        print("10. Export student progress report")
        print("11. Generate AI parent progress update") 
        print("12. Generate class performance summary")
        print("13. View AI history")
        print("14. Student AI Portfolio")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            print("\n=== Create Assessment ===\n")

            title = input("Assessment title: ").strip()
            assessment_type = input("Type [quiz]: ").strip() or "quiz"
            max_score_text = input("Max score [100]: ").strip() or "100"

            if not title:
                print("Title is required.")
                return

            max_score = float(max_score_text)

            assessment_id = self.toolkit.assessment_repository.save(
                teacher_id=self.toolkit.teacher_id,
                title=title,
                assessment_type=assessment_type,
                max_score=max_score,
            )

            print(f"\nAssessment saved with ID: {assessment_id}")
            return

        if choice == "2":
            assessments = self.toolkit.assessment_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not assessments:
                print("\nNo assessments found. Create one first.")
                return

            print("\n=== Assessments ===\n")

            for index, assessment in enumerate(assessments, start=1):
                print(
                    f"{index}. {assessment['title']} | Max: {assessment['max_score']}"
                )

            selected = input("\nChoose assessment: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(assessments):
                print("Invalid option.")
                return

            assessment = assessments[index]
            students = self.toolkit.student_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not students:
                print("\nNo students found. Add students first.")
                return

            print("\n=== Enter Scores ===\n")

            for student in students:
                name = f"{student['first_name']} {student['last_name']}".strip()
                score_text = input(
                    f"{name} score, blank to skip: "
                ).strip()

                if not score_text:
                    continue

                try:
                    self.toolkit.gradebook_repository.record_score(
                        student_id=student["id"],
                        assessment_id=assessment["id"],
                        score=float(score_text),
                        max_score=float(assessment["max_score"]),
                    )
                except ValueError as e:
                    print(f"Invalid score: {e}")


            print("\nScores saved.")
            return

        if choice == "3":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            results = self.toolkit.gradebook_repository.results_for_assessment(
                assessment["id"]
            )

            print("\n=== Assessment Results ===\n")

            if not results:
                print("No scores found.")
                return

            for row in results:
                name = f"{row['first_name']} {row['last_name']}".strip()
                print(
                    f"{name}: {row['score']} / {assessment['max_score']} ({row['percent']}%)"
                )

            return

        if choice == "4":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            threshold_text = input("Threshold percent [70]: ").strip() or "70"
            threshold = float(threshold_text)

            students = self.toolkit.gradebook_repository.struggling_students(
                assessment_id=assessment["id"],
                threshold=threshold,
            )

            print("\n=== Students Needing Support ===\n")

            if not students:
                print("No students below threshold.")
                return

            for row in students:
                name = f"{row['first_name']} {row['last_name']}".strip()
                print(f"{name}: {row['percent']}%")

            return

        if choice == "5":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            results = self.toolkit.gradebook_repository.results_for_assessment(
                assessment["id"]
            )

            if not results:
                print("\nNo scores found to export.")
                return

            output_path = self.toolkit.excel_exporter.export_assessment_results(
                assessment,
                results,
            )

            print(f"\nExcel exported: {output_path}")
            return

        if choice == "6":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            threshold_text = input("Threshold percent [70]: ").strip() or "70"
            threshold = float(threshold_text)

            all_results = self.toolkit.gradebook_repository.results_for_assessment(
                assessment["id"]
            )

            if not all_results:
                print(
                    "\nNo scores have been entered for this assessment yet."
                )
                return

            students = self.toolkit.gradebook_repository.struggling_students(
                assessment_id=assessment["id"],
                threshold=threshold,
            )

            print("\n=== Students Needing Support ===\n")

            if not students:
                print("All students are above the threshold.")
                return

            for row in students:
                name = (
                    f"{row['first_name']} "
                    f"{row['last_name']}"
                ).strip()

                print(
                    f"{name}: {row['percent']}%"
                )

            student_details = []

            for row in students:
                name = (
                    f"{row['first_name']} "
                    f"{row['last_name']}"
                ).strip()

                student_details.append(
                    f"{name}: {row['percent']}%"
                )

            grade = input("\nGrade level: ").strip()

            print("\nGenerating intervention plan...\n")

            result = self.toolkit.intervention_generator.generate(
                assessment_title=assessment["title"],
                students="\n".join(student_details),
                grade=grade,
            )
            self.toolkit.ai_history_repository.save(
                teacher_id=self.toolkit.teacher_id,
                assessment_id=assessment["id"],
                history_type="intervention",
                prompt=(
                    f"Assessment: {assessment['title']}\n"
                    f"Students:\n{chr(10).join(student_details)}"
                ),
                response=result,
            )

            metadata = {
                "title": (
                    f"Intervention for "
                    f"{assessment['title']}"
                ),
                "assessment": assessment["title"],
                "threshold": threshold,
                "students": ", ".join(student_details),
                "grade": grade,
            }

            self.toolkit.finish(
                result,
                "intervention",
                metadata=metadata,
            )

            return
        
        if choice == "7":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            threshold_text = input("Threshold percent [70]: ").strip() or "70"
            threshold = float(threshold_text)

            students = self.toolkit.gradebook_repository.struggling_students(
                assessment_id=assessment["id"],
                threshold=threshold,
            )

            if not students:
                print("\nNo students below threshold.")
                return

            student_details = []

            for row in students:
                name = (
                    f"{row['first_name']} "
                    f"{row['last_name']}"
                ).strip()

                student_details.append(
                    f"{name}: {row['percent']}%"
                )

            grade = input("\nGrade level: ").strip()
            topic = (
                f"Targeted practice for {assessment['title']} "
                f"for students needing support: "
                f"{'; '.join(student_details)}"
            )

            print("\nGenerating targeted intervention worksheet...\n")

            result = self.toolkit.worksheet_generator.generate(
                topic=topic,
                grade=grade,
                curriculum="Targeted intervention based on gradebook assessment results",
            )

            metadata = {
                "title": (
                    f"Intervention Worksheet for "
                    f"{assessment['title']}"
                ),
                "assessment": assessment["title"],
                "threshold": threshold,
                "students": "\n".join(student_details),
                "grade": grade,
                "topic": topic,
            }

            self.toolkit.finish(
                result,
                "worksheet",
                metadata=metadata,
            )

            return

        if choice == "8":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            threshold_text = input("Threshold percent [70]: ").strip() or "70"
            threshold = float(threshold_text)

            students = self.toolkit.gradebook_repository.struggling_students(
                assessment_id=assessment["id"],
                threshold=threshold,
            )

            if not students:
                print("\nNo students below threshold.")
                return

            student_details = []

            for row in students:
                name = (
                    f"{row['first_name']} "
                    f"{row['last_name']}"
                ).strip()

                student_details.append(
                    f"{name}: {row['percent']}%"
                )

            grade = input("\nGrade level: ").strip()

            topic = (
                f"Targeted intervention quiz for {assessment['title']} "
                f"for students needing support: "
                f"{'; '.join(student_details)}"
            )

            print("\nGenerating targeted intervention quiz...\n")

            result = self.toolkit.quiz_generator.generate(
                topic=topic,
                grade=grade,
                curriculum="Targeted intervention based on gradebook assessment results",
            )

            metadata = {
                "title": (
                    f"Intervention Quiz for "
                    f"{assessment['title']}"
                ),
                "assessment": assessment["title"],
                "threshold": threshold,
                "students": "\n".join(student_details),
                "grade": grade,
                "topic": topic,
            }

            self.toolkit.finish(
                result,
                "quiz",
                metadata=metadata,
            )

            return
        
        if choice == "9":
            students = self.toolkit.student_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not students:
                print("\nNo students found.")
                return

            print("\n=== Students ===\n")

            for index, student in enumerate(students, start=1):
                name = (
                    f"{student['first_name']} "
                    f"{student['last_name']}"
                ).strip()
                print(f"{index}. {name}")

            selected = input("\nChoose student: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(students):
                print("Invalid option.")
                return

            student = students[index]
            student_name = (
                f"{student['first_name']} "
                f"{student['last_name']}"
            ).strip()

            assessments = self.toolkit.assessment_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not assessments:
                print("\nNo assessments found.")
                return

            progress_rows = []

            for assessment in assessments:
                results = self.toolkit.gradebook_repository.results_for_assessment(
                    assessment["id"]
                )

                for row in results:
                    if row["student_id"] == student["id"]:
                        progress_rows.append(
                            {
                                "assessment": assessment["title"],
                                "score": row["score"],
                                "max_score": assessment["max_score"],
                                "percent": row["percent"],
                            }
                        )

            print(f"\n=== Progress Tracker: {student_name} ===\n")

            if not progress_rows:
                print("No scores found for this student.")
                return

            for row in progress_rows:
                print(
                    f"{row['assessment']}: "
                    f"{row['score']} / {row['max_score']} "
                    f"({row['percent']}%)"
                )

            if len(progress_rows) >= 2:
                first = progress_rows[0]["percent"]
                latest = progress_rows[-1]["percent"]
                growth = latest - first

                print("\n=== Growth Summary ===\n")
                print(f"First score: {first}%")
                print(f"Latest score: {latest}%")
                print(f"Growth: {growth:+.1f}%")

                if growth > 0:
                    print("Status: Improving")
                elif growth < 0:
                    print("Status: Needs continued support")
                else:
                    print("Status: No change yet")

            return

        if choice == "10":
            students = self.toolkit.student_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not students:
                print("\nNo students found.")
                return

            print("\n=== Students ===\n")

            for index, student in enumerate(students, start=1):
                name = (
                    f"{student['first_name']} "
                    f"{student['last_name']}"
                ).strip()
                print(f"{index}. {name}")

            selected = input("\nChoose student: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(students):
                print("Invalid option.")
                return

            student = students[index]
            student_name = (
                f"{student['first_name']} "
                f"{student['last_name']}"
            ).strip()

            assessments = self.toolkit.assessment_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            progress_rows = []

            for assessment in assessments:
                results = self.toolkit.gradebook_repository.results_for_assessment(
                    assessment["id"]
                )

                for row in results:
                    if row["student_id"] == student["id"]:
                        progress_rows.append(
                            {
                                "assessment": assessment["title"],
                                "score": row["score"],
                                "max_score": assessment["max_score"],
                                "percent": row["percent"],
                            }
                        )

            if not progress_rows:
                print("\nNo scores found for this student.")
                return

            report = f"# Student Progress Report: {student_name}\n\n"
            report += f"School: {self.toolkit.teacher_profile.school}\n\n"
            report += "## Assessment History\n\n"

            for row in progress_rows:
                report += (
                    f"- {row['assessment']}: "
                    f"{row['score']} / {row['max_score']} "
                    f"({row['percent']}%)\n"
                )

            if len(progress_rows) >= 2:
                first = progress_rows[0]["percent"]
                latest = progress_rows[-1]["percent"]
                growth = latest - first

                report += "\n## Growth Summary\n\n"
                report += f"- First score: {first}%\n"
                report += f"- Latest score: {latest}%\n"
                report += f"- Growth: {growth:+.1f}%\n"

                if growth > 0:
                    report += "- Status: Improving\n"
                elif growth < 0:
                    report += "- Status: Needs continued support\n"
                else:
                    report += "- Status: No change yet\n"

            metadata = {
                "title": f"Progress Report for {student_name}",
                "student": student_name,
            }

            self.toolkit.finish(
                report,
                "progress_report",
                metadata=metadata,
            )

            return

        if choice == "11":
            students = self.toolkit.student_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not students:
                print("\nNo students found.")
                return

            print("\n=== Students ===\n")

            for index, student in enumerate(students, start=1):
                name = (
                    f"{student['first_name']} "
                    f"{student['last_name']}"
                ).strip()
                print(f"{index}. {name}")

            selected = input("\nChoose student: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(students):
                print("Invalid option.")
                return

            student = students[index]
            student_name = (
                f"{student['first_name']} "
                f"{student['last_name']}"
            ).strip()

            assessments = self.toolkit.assessment_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            progress_rows = []

            for assessment in assessments:
                results = self.toolkit.gradebook_repository.results_for_assessment(
                    assessment["id"]
                )

                for row in results:
                    if row["student_id"] == student["id"]:
                        progress_rows.append(
                            {
                                "assessment": assessment["title"],
                                "score": row["score"],
                                "max_score": assessment["max_score"],
                                "percent": row["percent"],
                            }
                        )

            if not progress_rows:
                print("\nNo scores found for this student.")
                return

            progress_text = ""

            for row in progress_rows:
                progress_text += (
                    f"{row['assessment']}: "
                    f"{row['score']} / {row['max_score']} "
                    f"({row['percent']}%)\n"
                )

            prompt = (
                "Write a warm, professional parent progress update email.\n\n"
                f"Student: {student_name}\n"
                f"Gradebook data:\n{progress_text}\n"
                "Mention strengths, areas for continued practice, "
                "and one simple home support suggestion. "
                "Keep the tone encouraging and teacher-friendly. "
                "Do not include a subject line."
            )

            print("\nGenerating parent progress update...\n")

            result = self.toolkit.ai.chat(prompt)
            self.toolkit.ai_history_repository.save(
                teacher_id=self.toolkit.teacher_id,
                student_id=student["id"],
                history_type="parent_progress_update",
                prompt=prompt,
                response=result,
            )

            metadata = {
                "title": f"Parent Progress Update for {student_name}",
                "student": student_name,
            }

            self.toolkit.finish(
                result,
                "parent_progress_update",
                metadata=metadata,
            )

            return

        if choice == "12":
            assessment = self.toolkit._select_assessment()

            if not assessment:
                return

            results = self.toolkit.gradebook_repository.results_for_assessment(
                assessment["id"]
            )

            if not results:
                print("\nNo scores found.")
                return

            print("\nGenerating class performance summary...\n")

            total = 0
            high_students = []
            support_students = []

            class_data = ""

            for row in results:
                name = (
                    f"{row['first_name']} "
                    f"{row['last_name']}"
                ).strip()

                percent = row["percent"]

                total += percent

                class_data += (
                    f"{name}: {percent}%\n"
                )

                if percent >= 85:
                    high_students.append(name)

                if percent < 70:
                    support_students.append(name)


            average = total / len(results)


            prompt = (
                "You are an expert teacher analyzing class data.\n\n"
                f"Assessment: {assessment['title']}\n\n"
                f"Class Average: {average:.1f}%\n\n"
                "Student Results:\n"
                f"{class_data}\n\n"
                "Create a teacher class performance summary including:\n"
                "1. Overall performance\n"
                "2. Students showing mastery\n"
                "3. Students needing support\n"
                "4. Possible skill gaps\n"
                "5. Recommended small groups\n"
                "6. Next instructional steps\n\n"
                "Use professional teacher language."
            )


            result = self.toolkit.ai.chat(prompt)
            self.toolkit.ai_history_repository.save(
                teacher_id=self.toolkit.teacher_id,
                assessment_id=assessment["id"],
                history_type="class_summary",
                prompt=prompt,
                response=result,
            )


            metadata = {
                "title": (
                    f"Class Performance - "
                    f"{assessment['title']}"
                ),
                "assessment": assessment["title"],
                "average": average,
            }


            self.toolkit.finish(
                result,
                "class_summary",
                metadata=metadata,
            )

            return
        

        if choice == "13":
            history = self.toolkit.ai_history_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            print("\n=== AI History ===\n")

            if not history:
                print("No AI history found.")
                return

            for item in history:
                print(f"ID: {item['id']}")
                print(f"Type: {item['history_type']}")
                print(f"Created: {item['created_at']}")
                print("-" * 40)
                print(item["response"][:500])
                print("=" * 40)

            return

        if choice == "14":
            students = self.toolkit.student_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            if not students:
                print("\nNo students found.")
                return

            print("\n=== Students ===\n")

            for index, student in enumerate(students, start=1):
                name = (
                    f"{student['first_name']} "
                    f"{student['last_name']}"
                ).strip()
                print(f"{index}. {name}")

            selected = input("\nChoose student: ").strip()

            if not selected.isdigit():
                print("Invalid option.")
                return

            index = int(selected) - 1

            if index < 0 or index >= len(students):
                print("Invalid option.")
                return

            student = students[index]
            student_name = (
                f"{student['first_name']} "
                f"{student['last_name']}"
            ).strip()

            assessments = self.toolkit.assessment_repository.list_by_teacher(
                self.toolkit.teacher_id
            )

            progress_rows = []

            for assessment in assessments:
                results = self.toolkit.gradebook_repository.results_for_assessment(
                    assessment["id"]
                )

                for row in results:
                    if row["student_id"] == student["id"]:
                        progress_rows.append(
                            {
                                "assessment": assessment["title"],
                                "score": row["score"],
                                "max_score": assessment["max_score"],
                                "percent": row["percent"],
                                "created_at": row["created_at"],
                            }
                        )

            ai_history = self.toolkit.ai_history_repository.list_by_student(
                student["id"]
            )

            print(f"\n=== Student AI Portfolio: {student_name} ===\n")

            print("Assessment History")
            print("-" * 40)

            if not progress_rows:
                print("No assessment scores found.")
            else:
                for row in progress_rows:
                    print(
                        f"{row['assessment']}: "
                        f"{row['score']} / {row['max_score']} "
                        f"({row['percent']}%)"
                    )

            print("\nAI History")
            print("-" * 40)

            if not ai_history:
                print("No student-specific AI history found.")
            else:
                for item in ai_history:
                    print(f"{item['created_at']} | {item['history_type']}")
                    print(item["response"][:300])
                    print("-" * 40)

            if len(progress_rows) >= 2:
                first = progress_rows[0]["percent"]
                latest = progress_rows[-1]["percent"]
                growth = latest - first

                print("\nGrowth Summary")
                print("-" * 40)
                print(f"First score: {first}%")
                print(f"Latest score: {latest}%")
                print(f"Growth: {growth:+.1f}%")

                if growth > 0:
                    print("Status: Improving")
                elif growth < 0:
                    print("Status: Needs continued support")
                else:
                    print("Status: No change yet")

            return    
            
        print("Invalid option.")
    #END manage_gradebook
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook


class ExcelGradebookExporter:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_assessment_results(
        self,
        assessment: dict,
        results: list[dict],
    ) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = assessment["title"].lower().replace(" ", "_")
        output_path = self.output_dir / f"{safe_title}_{timestamp}.xlsx"

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Results"

        sheet.append([
            "Student",
            "Score",
            "Max Score",
            "Percent",
        ])

        max_score = assessment.get("max_score", 100)

        for row in results:
            student_name = f"{row['first_name']} {row['last_name']}".strip()

            sheet.append([
                student_name,
                row["score"],
                max_score,
                row["percent"],
            ])

        workbook.save(output_path)

        return output_path
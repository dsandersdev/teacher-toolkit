from datetime import datetime
from pathlib import Path

from docx import Document
from docx.shared import Pt


class DocxExporter:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save(
        self,
        content: str,
        prefix: str,
        metadata: dict | None = None,
    ) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"{prefix}_{timestamp}.docx"

        metadata = metadata or {}

        document = Document()

        styles = document.styles
        styles["Normal"].font.name = "Calibri"
        styles["Normal"].font.size = Pt(11)

        title = metadata.get("title", prefix.replace("_", " ").title())

        document.add_heading(title, level=0)

        if metadata.get("grade"):
            document.add_paragraph(f"Grade: {metadata['grade']}")

        if metadata.get("curriculum"):
            document.add_paragraph(f"Curriculum: {metadata['curriculum']}")

        document.add_paragraph("")

        for line in content.splitlines():
            clean_line = line.strip()

            if not clean_line:
                document.add_paragraph("")
                continue

            if clean_line.startswith("# "):
                document.add_heading(clean_line.replace("# ", ""), level=1)

            elif clean_line.startswith("## "):
                document.add_heading(clean_line.replace("## ", ""), level=2)

            elif clean_line.startswith("### "):
                document.add_heading(clean_line.replace("### ", ""), level=3)

            elif clean_line.startswith("- "):
                document.add_paragraph(
                    clean_line.replace("- ", ""),
                    style="List Bullet",
                )

            elif clean_line[0:2].isdigit() and clean_line[2:3] in [".", ")"]:
                document.add_paragraph(
                    clean_line,
                    style="List Number",
                )

            else:
                paragraph = document.add_paragraph(clean_line)
                paragraph.paragraph_format.space_after = Pt(6)

        document.save(output_path)

        return output_path
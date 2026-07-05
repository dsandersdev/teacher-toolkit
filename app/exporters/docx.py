from datetime import datetime
from pathlib import Path

from docx import Document


class DocxExporter:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save(self, content: str, prefix: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"{prefix}_{timestamp}.docx"

        document = Document()

        for line in content.splitlines():
            if line.startswith("# "):
                document.add_heading(line.replace("# ", ""), level=1)
            elif line.startswith("## "):
                document.add_heading(line.replace("## ", ""), level=2)
            elif line.startswith("### "):
                document.add_heading(line.replace("### ", ""), level=3)
            elif line.strip() == "":
                document.add_paragraph("")
            else:
                document.add_paragraph(line)

        document.save(output_path)

        return output_path
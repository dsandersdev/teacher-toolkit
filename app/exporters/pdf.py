from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class PdfExporter:
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
        output_path = self.output_dir / f"{prefix}_{timestamp}.pdf"

        metadata = metadata or {}
        title = metadata.get("title", prefix.replace("_", " ").title())

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=LETTER,
        )

        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))

        for key, value in metadata.items():
            story.append(
                Paragraph(
                    f"<b>{key.replace('_', ' ').title()}:</b> {value}",
                    styles["Normal"],
                )
            )

        story.append(Spacer(1, 12))

        for line in content.splitlines():
            clean_line = line.strip()

            if not clean_line:
                story.append(Spacer(1, 8))
                continue

            if clean_line.startswith("# "):
                story.append(Paragraph(clean_line[2:], styles["Heading1"]))
            elif clean_line.startswith("## "):
                story.append(Paragraph(clean_line[3:], styles["Heading2"]))
            elif clean_line.startswith("### "):
                story.append(Paragraph(clean_line[4:], styles["Heading3"]))
            elif clean_line.startswith("- "):
                story.append(Paragraph(f"• {clean_line[2:]}", styles["Normal"]))
            else:
                story.append(Paragraph(clean_line, styles["Normal"]))

            story.append(Spacer(1, 6))

        document.build(story)

        return output_path
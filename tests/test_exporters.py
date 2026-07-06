from pathlib import Path

from app.exporters.docx import DocxExporter
from app.exporters.pdf import PdfExporter


def test_docx_export_creates_file(tmp_path):
    exporter = DocxExporter(output_dir=tmp_path)

    output = exporter.save(
        content="# Test Lesson\n\n- item one",
        prefix="test",
        metadata={
            "title": "Test Lesson",
            "grade": "2",
        },
    )

    assert output.exists()
    assert output.suffix == ".docx"

def test_pdf_export_creates_file(tmp_path):
    exporter = PdfExporter(output_dir=tmp_path)

    output = exporter.save(
        content="# Test Lesson\n\n- item one",
        prefix="test",
        metadata={
            "title": "Test PDF",
            "grade": "2",
        },
    )

    assert output.exists()
    assert output.suffix == ".pdf"
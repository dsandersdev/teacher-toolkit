import json

from app.storage.library import ResourceLibrary


def test_resource_library_loads_json_resources(tmp_path):
    resource_file = tmp_path / "lesson_001.json"

    resource_file.write_text(
        json.dumps(
            {
                "id": "lesson_001",
                "type": "lesson",
                "created_at": "2026-07-05T18:00:00",
                "metadata": {
                    "title": "Addition Lesson",
                    "topic": "Addition within 20",
                    "grade": "2",
                },
                "content": "Students practice addition facts.",
            }
        ),
        encoding="utf-8",
    )

    library = ResourceLibrary(output_dir=tmp_path)

    resources = library.all()

    assert len(resources) == 1
    assert resources[0]["id"] == "lesson_001"
    assert resources[0]["type"] == "lesson"


def test_resource_library_finds_by_type(tmp_path):
    (tmp_path / "lesson.json").write_text(
        json.dumps({"type": "lesson", "content": "Lesson content"}),
        encoding="utf-8",
    )

    (tmp_path / "quiz.json").write_text(
        json.dumps({"type": "quiz", "content": "Quiz content"}),
        encoding="utf-8",
    )

    library = ResourceLibrary(output_dir=tmp_path)

    lessons = library.find_by_type("lesson")

    assert len(lessons) == 1
    assert lessons[0]["type"] == "lesson"


def test_resource_library_searches_content(tmp_path):
    (tmp_path / "worksheet.json").write_text(
        json.dumps(
            {
                "type": "worksheet",
                "metadata": {
                    "title": "Subtraction Worksheet",
                    "topic": "Subtraction",
                    "grade": "2",
                },
                "content": "Practice subtraction problems.",
            }
        ),
        encoding="utf-8",
    )

    library = ResourceLibrary(output_dir=tmp_path)

    results = library.search("subtraction")

    assert len(results) == 1
    assert results[0]["type"] == "worksheet"
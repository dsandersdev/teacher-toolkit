from app.generators.lesson import LessonGenerator
from app.generators.worksheet import WorksheetGenerator
from app.generators.parent_email import ParentEmailGenerator
from app.generators.report_comment import ReportCommentGenerator


GENERATOR_REGISTRY = {
    "1": {
        "name": "Lesson plan",
        "prefix": "lesson_plan",
        "class": LessonGenerator,
        "fields": {
            "grade": "2nd Grade",
            "topic": "",
            "curriculum": None,
        },
    },
    "2": {
        "name": "Worksheet",
        "prefix": "worksheet",
        "class": WorksheetGenerator,
        "fields": {
            "grade": "2nd Grade",
            "topic": "",
            "curriculum": None,
        },
    },
    "3": {
        "name": "Parent email",
        "prefix": "parent_email",
        "class": ParentEmailGenerator,
        "fields": {
            "situation": "",
        },
    },
    "4": {
        "name": "Report card comment",
        "prefix": "report_comment",
        "class": ReportCommentGenerator,
        "fields": {
            "student_name": "",
            "strengths": "",
            "growth": "",
        },
    },
}
from dataclasses import dataclass, asdict


@dataclass
class TeacherProfile:
    name: str
    school: str = ""
    grades: list[str] | None = None
    subjects: list[str] | None = None
    curriculum: str = ""
    teaching_style: str = ""

    def to_dict(self):
        return asdict(self)
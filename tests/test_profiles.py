from app.users.profile import TeacherProfile
from app.users.manager import ProfileManager


def test_teacher_profile_save_and_load(tmp_path):
    manager = ProfileManager(profile_dir=tmp_path)

    profile = TeacherProfile(
        name="test_teacher",
        school="Test School",
        grades=["2nd Grade"],
        subjects=["Math"],
        curriculum="General",
        teaching_style="hands-on",
    )

    manager.save(profile)

    loaded = manager.load("test_teacher")

    assert loaded.name == "test_teacher"
    assert loaded.school == "Test School"
    assert loaded.grades == ["2nd Grade"]
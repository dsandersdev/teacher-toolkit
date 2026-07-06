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

def test_profile_manager_lists_profiles(tmp_path):
    manager = ProfileManager(profile_dir=tmp_path)

    profile = TeacherProfile(
        name="Test Teacher",
        school="Test School",
    )

    manager.save(profile)

    profiles = manager.list_profiles()

    assert len(profiles) == 1
    assert profiles[0]["name"] == "Test Teacher"


def test_profile_manager_active_profile(tmp_path):
    manager = ProfileManager(profile_dir=tmp_path)

    profile = TeacherProfile(
        name="Active Teacher",
        school="Active School",
    )

    manager.save(profile)

    manager.set_active("active_teacher")

    active = manager.get_active()

    assert active.name == "Active Teacher"
    assert active.school == "Active School"
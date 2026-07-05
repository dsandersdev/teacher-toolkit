from app.registry import GENERATOR_REGISTRY


def test_registry_has_expected_generators():
    names = [
        item["name"]
        for item in GENERATOR_REGISTRY.values()
    ]

    assert "Lesson plan" in names
    assert "Worksheet" in names
    assert "Parent email" in names
    assert "Report card comment" in names
    assert "Quiz" in names


def test_registry_entries_have_required_keys():
    for item in GENERATOR_REGISTRY.values():
        assert "name" in item
        assert "prefix" in item
        assert "class" in item
        assert "fields" in item


def test_registry_prefixes_are_unique():
    prefixes = [
        item["prefix"]
        for item in GENERATOR_REGISTRY.values()
    ]

    assert len(prefixes) == len(set(prefixes))
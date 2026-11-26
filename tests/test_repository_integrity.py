from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVELS = {"basics": 8, "intermediate": 8, "advanced": 9}


def test_every_topic_has_the_complete_student_package():
    required_sections = (
        "## Topic explanation",
        "## Solved practical example",
        "## Code exercise",
        "### Example input and expected output",
        "## Artificial Intelligence (AI) review",
        "## Unit test",
    )
    for level, expected_count in LEVELS.items():
        topics = sorted(path for path in (ROOT / level).iterdir() if path.is_dir())
        assert len(topics) == expected_count
        for topic in topics:
            readme = (topic / "README.md").read_text(encoding="utf-8")
            for section in required_sections:
                assert section in readme, f"{topic.relative_to(ROOT)} is missing {section}"
            assert (topic / "AI_REVIEW_PROMPT.md").is_file()
            assert (topic / "tests" / "test_homework.py").is_file()
            assert any((topic / name).is_file() for name in ("homework.py", "homework.sql", "homework.md"))


def test_reference_tree_is_complete_and_contains_no_placeholders():
    for level, expected_count in LEVELS.items():
        source_topics = sorted(path for path in (ROOT / level).iterdir() if path.is_dir())
        solution_topics = sorted(path for path in (ROOT / "solutions" / level).iterdir() if path.is_dir())
        assert [path.name for path in solution_topics] == [path.name for path in source_topics]
        assert len(solution_topics) == expected_count
        for topic in solution_topics:
            homework = next(
                topic / name
                for name in ("homework.py", "homework.sql", "homework.md")
                if (topic / name).is_file()
            )
            text = homework.read_text(encoding="utf-8")
            assert "TODO" not in text
            assert "NotImplemented" not in text

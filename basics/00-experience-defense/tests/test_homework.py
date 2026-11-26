import re

from test_support import homework_path


def test_story_has_required_evidence():
    text = homework_path(__file__, "homework.md").read_text(encoding="utf-8")
    assert "TODO" not in text
    for heading in ("90-second", "Scale", "decisions", "Failure", "change now"):
        assert heading.lower() in text.lower()
    assert len(text.split()) >= 180
    assert len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text)) >= 3


def test_story_names_ownership_and_tradeoff():
    text = homework_path(__file__, "homework.md").read_text(encoding="utf-8").lower()
    assert any(term in text for term in ("i designed", "i implemented", "i led", "i decided"))
    assert any(term in text for term in ("instead of", "rejected", "alternative", "trade-off", "tradeoff"))

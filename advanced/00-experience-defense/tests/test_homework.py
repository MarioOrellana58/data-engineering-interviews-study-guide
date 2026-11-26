import re

from test_support import homework_path


def test_story_bank_is_substantive_and_consistent_in_shape():
    text = homework_path(__file__, "homework.md").read_text(encoding="utf-8")
    assert "TODO" not in text
    assert len(text.split()) >= 700
    assert len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text)) >= 12
    for term in ("architecture story", "incident story", "leadership story", "consistency matrix", "mistake"):
        assert term in text.lower()
    assert text.count("|") >= 12

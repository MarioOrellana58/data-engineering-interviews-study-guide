import re

from test_support import homework_path


def test_deep_dive_contains_evidence_and_diagram():
    text = homework_path(__file__, "homework.md").read_text(encoding="utf-8")
    assert "TODO" not in text
    assert "```mermaid" in text
    assert len(text.split()) >= 350
    assert len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text)) >= 6
    for term in ("slo", "cost", "failure", "alternative", "contribution", "question map"):
        assert term in text.lower()

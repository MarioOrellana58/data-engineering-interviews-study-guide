import pytest

from test_support import load_homework

hw = load_homework(__file__)


def test_deduplicates_versions_quarantines_bad_and_checkpoints():
    pages = {
        None: {"items": [{"id": "a", "version": 1, "body": "x"}, {"id": "bad"}], "next_token": "t1", "source": "api"},
        "t1": {"items": [{"id": "a", "version": 1, "body": "x"}, {"id": "a", "version": 2, "body": "y"}], "next_token": None, "source": "api"},
    }
    result = hw.ingest_pages(lambda token: pages[token], None, set(), 10)
    assert [(x["id"], x["version"]) for x in result["accepted"]] == [("a", 1), ("a", 2)]
    assert all(x.get("source") == "api" for x in result["accepted"])
    assert len(result["quarantined"]) == 1
    assert result["next_token"] is None


def test_cycle_and_page_bound_are_enforced():
    def cyclic(token):
        return {"items": [], "next_token": "same", "source": "api"}

    with pytest.raises(ValueError, match="cycle"):
        hw.ingest_pages(cyclic, "same", set(), 5)

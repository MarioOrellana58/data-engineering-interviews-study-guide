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


def test_page_bound_returns_a_resumable_checkpoint():
    calls = []
    pages = {
        None: {"items": [{"id": "a", "version": 1, "body": "x"}], "next_token": "t1", "source": "api"},
        "t1": {"items": [{"id": "b", "version": 1, "body": "y"}], "next_token": "t2", "source": "api"},
    }

    def fetch(token):
        calls.append(token)
        return pages[token]

    result = hw.ingest_pages(fetch, None, set(), max_pages=1)
    assert calls == [None]
    assert [(x["id"], x["version"]) for x in result["accepted"]] == [("a", 1)]
    assert result["next_token"] == "t1"


def test_provenance_is_complete_and_deterministic():
    page = {"items": [{"id": "a", "version": 1, "body": {"z": 2, "a": 1}}],
            "next_token": None, "source": "partner", "source_url": "https://example.test/page/1",
            "retrieved_at": "2026-01-01T00:00:00Z"}
    one = hw.ingest_pages(lambda _: page, None, set(), 1)["accepted"][0]
    two = hw.ingest_pages(lambda _: page, None, set(), 1)["accepted"][0]
    assert one == two
    assert one["source_url"] == page["source_url"]
    assert one["retrieved_at"] == page["retrieved_at"]
    assert len(one["content_hash"]) == 64


def test_malformed_page_and_token_are_rejected():
    with pytest.raises(ValueError, match="items list"):
        hw.ingest_pages(lambda _: {"items": "not-a-list"}, None, set(), 1)
    with pytest.raises(ValueError, match="next_token"):
        hw.ingest_pages(lambda _: {"items": [], "next_token": 123}, None, set(), 1)

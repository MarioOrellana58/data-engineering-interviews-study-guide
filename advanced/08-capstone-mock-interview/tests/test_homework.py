from copy import deepcopy

from test_support import homework_path, load_homework

hw = load_homework(__file__)


def test_batch_is_secure_deterministic_and_replay_safe():
    existing = {"a": {"id": "a", "source_version": 1, "email_token": "old", "amount": 1}}
    events = [
        {"event_id": "e2", "id": "a", "op": "upsert", "source_version": 2, "email": "Ada@Example.com", "amount": 2},
        {"event_id": "e1", "id": "b", "op": "upsert", "source_version": 1, "email": "b@example.com", "amount": 3},
        {"event_id": "e3", "id": "bad", "op": "upsert", "source_version": 1, "amount": "NaN"},
    ]
    before = deepcopy((existing, events))
    one = hw.process_batch(existing, events, "interview-secret")
    two = hw.process_batch(existing, list(reversed(events)), "interview-secret")
    assert (existing, events) == before
    assert one == two
    assert one["published"] == two["published"]
    assert "ada@example.com" not in str(one["published"]).lower()
    assert all("email" not in row for row in one["published"].values())
    assert one["published"]["a"]["email_token"]
    assert one["published"]["a"]["source_version"] == 2
    assert len(one["quarantined"]) == 1
    assert one["metrics"]["input_count"] == 3
    replay = hw.process_batch(one["published"], events, "interview-secret")
    assert replay["published"] == one["published"]
    other_secret = hw.process_batch(existing, events, "rotated-secret")
    assert other_secret["published"]["a"]["email_token"] != one["published"]["a"]["email_token"]


def test_tombstone_and_stale_version_semantics():
    existing = {"x": {"id": "x", "source_version": 5, "email_token": "t", "amount": 1}}
    events = [
        {"event_id": "old", "id": "x", "op": "upsert", "source_version": 4, "email": "x@x.com", "amount": 99},
        {"event_id": "del", "id": "x", "op": "delete", "source_version": 6},
    ]
    result = hw.process_batch(existing, events, "secret")
    assert "x" not in result["published"]
    assert result["metrics"]["stale_count"] == 1


def test_durable_tombstone_blocks_stale_resurrection_across_batches():
    existing = {"x": {"id": "x", "source_version": 5, "email_token": "t", "amount": 1}}
    deleted = hw.process_batch(existing, [{"event_id": "del", "id": "x", "op": "delete", "source_version": 6}], "secret")
    stale = {"event_id": "old", "id": "x", "op": "upsert", "source_version": 4, "email": "x@example.com", "amount": 9}
    replayed = hw.process_batch(deleted["state"], [stale], "secret")
    assert "x" not in replayed["published"]
    assert replayed["metrics"]["stale_count"] == 1


def test_existing_raw_email_is_sanitized_and_conflicts_are_quarantined():
    existing = {"x": {"id": "x", "source_version": 2, "email": "X@Example.com", "amount": 1}}
    conflict = {"event_id": "other", "id": "x", "op": "upsert", "source_version": 2, "email": "other@example.com", "amount": 2}
    result = hw.process_batch(existing, [conflict], "secret")
    assert "email" not in result["published"]["x"]
    assert result["published"]["x"]["email_token_version"] == "v1"
    assert result["quarantined"][0]["reason"] == "source_version conflicts with existing state"


def test_boolean_version_and_amount_are_not_accepted_as_integers():
    events = [
        {"event_id": "bad-version", "id": "x", "op": "delete", "source_version": True},
        {"event_id": "bad-amount", "id": "y", "op": "upsert", "source_version": 1, "email": "y@example.com", "amount": False},
    ]
    assert hw.process_batch({}, events, "secret")["metrics"]["quarantined_count"] == 2


def test_explicit_key_version_is_published_for_rotation():
    event = {"event_id": "e", "id": "x", "op": "upsert", "source_version": 1,
             "email": "x@example.com", "amount": 1}
    old = hw.process_batch({}, [event], "v1:old-secret")["published"]["x"]
    new = hw.process_batch({}, [event], "v2:new-secret")["published"]["x"]
    assert old["email_token_version"] == "v1"
    assert new["email_token_version"] == "v2"
    assert old["email_token"] != new["email_token"]


def test_design_is_complete_and_quantified():
    text = homework_path(__file__, "DESIGN.md").read_text(encoding="utf-8")
    assert "TODO" not in text
    assert len(text.split()) >= 900
    for term in ("250,000", "residency", "rpo", "rto", "cost", "snowflake", "databricks", "replay"):
        assert term in text.lower()

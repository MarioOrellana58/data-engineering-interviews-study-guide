import hashlib
import hmac
import math
from copy import deepcopy


def _email_token(email: str, secret: str) -> str:
    normalized = email.strip().lower().encode()
    return hmac.new(secret.encode(), normalized, hashlib.sha256).hexdigest()


def _invalid(event: dict) -> str | None:
    required = {"event_id", "id", "op", "source_version"}
    if not required.issubset(event):
        return "missing required fields"
    if event["op"] not in {"upsert", "delete"}:
        return "unsupported operation"
    if not isinstance(event["source_version"], int):
        return "source_version must be an integer"
    if event["op"] == "upsert":
        if not isinstance(event.get("email"), str) or "@" not in event["email"]:
            return "invalid email"
        if not isinstance(event.get("amount"), (int, float)) or not math.isfinite(float(event["amount"])):
            return "amount must be finite"
    return None


def process_batch(existing: dict[str, dict], events: list[dict], pii_secret: str) -> dict:
    if not pii_secret:
        raise ValueError("pii_secret must not be empty")
    published = deepcopy(existing)
    quarantined = []
    stale_count = deletion_count = upsert_count = 0
    seen_event_ids = set()

    ordered = sorted(
        (deepcopy(event) for event in events),
        key=lambda row: (
            str(row.get("id", "")),
            row.get("source_version") if isinstance(row.get("source_version"), int) else -1,
            str(row.get("event_id", "")),
        ),
    )
    for event in ordered:
        reason = _invalid(event)
        if reason:
            event["reason"] = reason
            quarantined.append(event)
            continue
        if event["event_id"] in seen_event_ids:
            stale_count += 1
            continue
        seen_event_ids.add(event["event_id"])

        current = published.get(event["id"])
        if current is not None and event["source_version"] <= current["source_version"]:
            stale_count += 1
            continue
        if event["op"] == "delete":
            published.pop(event["id"], None)
            deletion_count += 1
        else:
            published[event["id"]] = {
                "id": event["id"],
                "source_version": event["source_version"],
                "email_token": _email_token(event["email"], pii_secret),
                "amount": event["amount"],
            }
            upsert_count += 1

    return {
        "published": {key: published[key] for key in sorted(published)},
        "quarantined": sorted(quarantined, key=lambda row: str(row.get("event_id", ""))),
        "metrics": {
            "input_count": len(events),
            "published_count": len(published),
            "upsert_count": upsert_count,
            "deletion_count": deletion_count,
            "stale_count": stale_count,
            "quarantined_count": len(quarantined),
        },
    }

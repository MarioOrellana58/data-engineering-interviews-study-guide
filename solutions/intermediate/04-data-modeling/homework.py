import hashlib
import json
from collections import defaultdict


def _surrogate_key(customer_id: str, valid_from: str, attributes: dict) -> str:
    payload = json.dumps([customer_id, valid_from, attributes], sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def build_scd2(changes: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for change in changes:
        grouped[change["customer_id"]].append(dict(change))

    result = []
    for customer_id in sorted(grouped):
        ordered = sorted(grouped[customer_id], key=lambda row: (row["at"], json.dumps(row, sort_keys=True)))
        versions = []
        for change in ordered:
            attributes = {key: value for key, value in change.items() if key not in {"customer_id", "at"}}
            if versions and versions[-1]["attributes"] == attributes:
                continue
            versions.append({"at": change["at"], "attributes": attributes})

        for index, version in enumerate(versions):
            valid_to = versions[index + 1]["at"] if index + 1 < len(versions) else None
            row = {
                "customer_sk": _surrogate_key(customer_id, version["at"], version["attributes"]),
                "customer_id": customer_id,
                **version["attributes"],
                "valid_from": version["at"],
                "valid_to": valid_to,
                "is_current": valid_to is None,
            }
            result.append(row)
    return result

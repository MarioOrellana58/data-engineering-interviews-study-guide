from __future__ import annotations

from datetime import date


def choose_storage(workload: dict) -> dict:
    if workload.get("point_reads") and workload.get("transactions") and not workload.get("large_scans"):
        return {
            "technology": "PostgreSQL",
            "format": "row store",
            "reasons": [
                "Indexed point reads avoid scanning unrelated rows.",
                "ACID transactions protect multi-row business updates.",
            ],
        }
    if workload.get("large_scans"):
        return {
            "technology": "object storage lakehouse",
            "format": "Parquet",
            "reasons": [
                "Columnar encoding reduces bytes read by analytical scans.",
                "Open files support independent compute and schema evolution.",
            ],
        }
    return {
        "technology": "relational row store",
        "format": "row store",
        "reasons": ["The access pattern is mixed and modest.", "A relational model keeps operational complexity low."],
    }


def files_to_scan(partitions: list[dict], start: date, end: date) -> list[str]:
    if start > end:
        raise ValueError("start must not be after end")
    selected = (part for part in partitions if start <= part["date"] <= end)
    return [part["path"] for part in sorted(selected, key=lambda part: (part["date"], part["path"]))]

from __future__ import annotations

from datetime import date


def choose_storage(workload: dict) -> dict:
    raise NotImplementedError


def files_to_scan(partitions: list[dict], start: date, end: date) -> list[str]:
    raise NotImplementedError

from __future__ import annotations


def process_events(existing: list[dict], incoming: list[dict]) -> dict:
    """Return {'published': [...], 'rejected': [...]} without mutating inputs."""
    raise NotImplementedError

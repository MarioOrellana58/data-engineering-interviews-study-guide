def build_bitemporal(changes: list[dict]) -> list[dict]:
    raise NotImplementedError


def as_of(rows: list[dict], entity_id: str, valid_at: str, known_at: str) -> dict | None:
    raise NotImplementedError

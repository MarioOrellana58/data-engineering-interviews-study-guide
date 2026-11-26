from collections.abc import Callable


def ingest_pages(
    fetch_page: Callable[[str | None], dict],
    start_token: str | None,
    seen_versions: set[tuple[str, int]],
    max_pages: int,
) -> dict:
    raise NotImplementedError

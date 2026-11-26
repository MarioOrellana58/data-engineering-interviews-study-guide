from collections.abc import Iterable, Iterator


def reconcile_sorted(
    left: Iterable[tuple[str, str]], right: Iterable[tuple[str, str]]
) -> Iterator[dict]:
    raise NotImplementedError

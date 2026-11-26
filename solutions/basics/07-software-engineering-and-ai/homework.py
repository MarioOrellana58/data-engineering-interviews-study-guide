from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_call(
    operation: Callable[[], T],
    is_transient: Callable[[Exception], bool],
    *,
    max_attempts: int,
    base_delay: float,
    max_delay: float,
) -> tuple[T, list[float]]:
    if max_attempts < 1 or base_delay < 0 or max_delay < 0 or base_delay > max_delay:
        raise ValueError("invalid retry configuration")

    delays = []
    for attempt in range(max_attempts):
        try:
            return operation(), delays
        except Exception as error:
            if not is_transient(error) or attempt == max_attempts - 1:
                raise
            delays.append(min(base_delay * (2**attempt), max_delay))
    raise AssertionError("unreachable")

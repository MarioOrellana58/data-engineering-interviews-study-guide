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
    raise NotImplementedError

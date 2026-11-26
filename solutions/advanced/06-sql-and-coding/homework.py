from collections.abc import Iterable, Iterator


def reconcile_sorted(
    left: Iterable[tuple[str, str]], right: Iterable[tuple[str, str]]
) -> Iterator[dict]:
    left_iterator, right_iterator = iter(left), iter(right)
    left_previous = right_previous = None

    def advance(iterator, previous):
        try:
            item = next(iterator)
        except StopIteration:
            return None, previous
        if previous is not None and item[0] <= previous:
            raise ValueError("keys must be unique and strictly ascending")
        return item, item[0]

    left_item, left_previous = advance(left_iterator, left_previous)
    right_item, right_previous = advance(right_iterator, right_previous)
    while left_item is not None or right_item is not None:
        if right_item is None or (left_item is not None and left_item[0] < right_item[0]):
            yield {"key": left_item[0], "status": "missing_right", "left_checksum": left_item[1], "right_checksum": None}
            left_item, left_previous = advance(left_iterator, left_previous)
        elif left_item is None or right_item[0] < left_item[0]:
            yield {"key": right_item[0], "status": "missing_left", "left_checksum": None, "right_checksum": right_item[1]}
            right_item, right_previous = advance(right_iterator, right_previous)
        else:
            if left_item[1] != right_item[1]:
                yield {"key": left_item[0], "status": "mismatch", "left_checksum": left_item[1], "right_checksum": right_item[1]}
            left_item, left_previous = advance(left_iterator, left_previous)
            right_item, right_previous = advance(right_iterator, right_previous)

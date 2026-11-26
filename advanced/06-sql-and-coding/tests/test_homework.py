import pytest

from test_support import load_homework

hw = load_homework(__file__)


class SinglePass:
    def __init__(self, values):
        self.values = iter(values)
        self.iterated = False

    def __iter__(self):
        if self.iterated:
            raise AssertionError("iterated twice")
        self.iterated = True
        return self.values


def test_linear_merge_results_and_single_pass_inputs():
    left = SinglePass([("a", "1"), ("b", "2"), ("d", "4")])
    right = SinglePass([("b", "X"), ("c", "3"), ("d", "4")])
    assert list(hw.reconcile_sorted(left, right)) == [
        {"key": "a", "status": "missing_right", "left_checksum": "1", "right_checksum": None},
        {"key": "b", "status": "mismatch", "left_checksum": "2", "right_checksum": "X"},
        {"key": "c", "status": "missing_left", "left_checksum": None, "right_checksum": "3"},
    ]


def test_duplicate_or_descending_keys_fail():
    with pytest.raises(ValueError):
        list(hw.reconcile_sorted([("b", "1"), ("a", "2")], []))
    with pytest.raises(ValueError):
        list(hw.reconcile_sorted([], [("a", "1"), ("a", "2")]))

import pytest

from test_support import load_homework

hw = load_homework(__file__)


class TransientError(RuntimeError):
    pass


def test_retries_transient_errors_with_bounded_backoff():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        if calls < 4:
            raise TransientError("try again")
        return "ok"

    value, delays = hw.retry_call(operation, lambda e: isinstance(e, TransientError), max_attempts=5, base_delay=2, max_delay=5)
    assert value == "ok"
    assert calls == 4
    assert delays == [2, 4, 5]


def test_non_transient_and_invalid_configuration_fail_fast():
    with pytest.raises(ValueError, match="bad request"):
        hw.retry_call(lambda: (_ for _ in ()).throw(ValueError("bad request")), lambda e: False, max_attempts=3, base_delay=1, max_delay=2)
    with pytest.raises(ValueError):
        hw.retry_call(lambda: 1, lambda e: False, max_attempts=0, base_delay=1, max_delay=2)


@pytest.mark.parametrize("attempts,base,maximum", [(True, 1, 2), (2, float("nan"), 2), (2, 1, float("inf"))])
def test_boolean_attempts_and_non_finite_delays_are_rejected(attempts, base, maximum):
    with pytest.raises(ValueError):
        hw.retry_call(lambda: 1, lambda _: False, max_attempts=attempts, base_delay=base, max_delay=maximum)

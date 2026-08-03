import pytest

from shop import apply_tax, grand_total


def test_order_total_includes_tax() -> None:
    assert grand_total([("api-call", 3, 1.0)], rate=0.1) == 3.3


def test_apply_tax_rejects_negative_rate() -> None:
    with pytest.raises(ValueError, match="negative"):
        apply_tax(10.0, rate=-0.1)

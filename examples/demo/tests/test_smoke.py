import pytest

from shop import grand_total, subtotal


@pytest.mark.smoke
def test_shop_module_prices_an_empty_cart() -> None:
    assert subtotal([]) == 0.0
    assert grand_total([]) == 0.0

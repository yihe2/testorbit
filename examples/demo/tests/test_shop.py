from shop import apply_tax, grand_total, subtotal


def test_subtotal_sums_line_items() -> None:
    items = [("coffee", 2, 3.5), ("muffin", 1, 2.25)]

    assert subtotal(items) == 9.25


def test_apply_tax_uses_default_rate() -> None:
    assert apply_tax(10.0) == 11.3


def test_grand_total_combines_subtotal_and_tax() -> None:
    assert grand_total([("tea", 1, 4.0)]) == 4.52

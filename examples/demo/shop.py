from __future__ import annotations


def subtotal(items: list[tuple[str, int, float]]) -> float:
    return round(sum(qty * price for _, qty, price in items), 2)


def apply_tax(amount: float, rate: float = 0.13) -> float:
    if rate < 0:
        raise ValueError("Tax rate cannot be negative.")
    return round(amount * (1 + rate), 2)


def grand_total(items: list[tuple[str, int, float]], rate: float = 0.13) -> float:
    return apply_tax(subtotal(items), rate)

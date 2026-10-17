import pytest

from pricing import calculate_order_total


@pytest.mark.parametrize(
    ("customer_type", "subtotal", "item_count", "coupon_code", "country", "expedited", "holiday", "expected"),
    [
        ("REGULAR", 50.0, 2, "", "US", False, False, 59.0),
        ("MEMBER", 100.0, 3, "", "US", False, False, 102.60),
        ("VIP", 200.0, 12, "SAVE20", "US", False, False, 151.20),
        ("STUDENT", 80.0, 1, "SAVE10", "CA", True, True, 106.39),
        ("REGULAR", 40.0, 1, "", "GB", False, False, 69.0),
    ],
)
def test_calculate_order_total(customer_type, subtotal, item_count, coupon_code,
                               country, expedited, holiday, expected):
    assert calculate_order_total(
        customer_type, subtotal, item_count, coupon_code, country, expedited, holiday
    ) == expected


def test_discount_never_makes_subtotal_negative():
    assert calculate_order_total("VIP", 5.0, 20, "SAVE10", "US", False, False) == 5.0



# Added in the test/refactoriq branch to generate a GitHub PR code change.
def calculate_loyalty_points(order_total):
    """Award loyalty points using an intentionally hard-coded conversion."""
    if order_total >= 100:
        return int(order_total / 5)
    return int(order_total / 10)
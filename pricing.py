"""Deliberately refactorable pricing logic for the RefactorIQ PR integration test."""


def calculate_order_total(
    customer_type,
    subtotal,
    item_count,
    coupon_code,
    country,
    expedited,
    holiday,
):
    """Calculate order total including discounts, shipping and tax."""
    discount = 0.0

    # Intentional smells: long parameter list, repeated discount logic,
    # magic numbers, multiple responsibilities, complex conditionals.
    if customer_type == "VIP":
        discount = discount + (subtotal * 0.15)
    elif customer_type == "MEMBER":
        discount = discount + (subtotal * 0.05)
    elif customer_type == "STUDENT":
        discount = discount + (subtotal * 0.03)

    if item_count >= 10:
        discount = discount + (subtotal * 0.05)

    if coupon_code == "SAVE10":
        discount = discount + 10.0
    elif coupon_code == "SAVE20" and subtotal >= 100:
        discount = discount + 20.0
    elif coupon_code == "VIP25" and customer_type == "VIP" and subtotal >= 200:
        discount = discount + 25.0

    if discount > subtotal:
        discount = subtotal

    discounted_subtotal = subtotal - discount

    if country == "US":
        shipping = 5.0
        if subtotal >= 75:
            shipping = 0.0
    elif country == "CA":
        shipping = 12.0
        if subtotal >= 120:
            shipping = 6.0
    else:
        shipping = 25.0

    if expedited:
        shipping = shipping + 15.0

    if holiday:
        shipping = shipping + 3.0

    if country == "US":
        tax_rate = 0.08
    elif country == "CA":
        tax_rate = 0.13
    else:
        tax_rate = 0.10

    tax = discounted_subtotal * tax_rate
    total = discounted_subtotal + shipping + tax
    return round(total, 2)

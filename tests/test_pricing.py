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

# ---------------------------------------------------------------------------
# Intentional code smells for RefactorIQ detection testing.
# Everything below works and is covered by tests, but is deliberately smelly.
# ---------------------------------------------------------------------------

# Smell: mutable global state shared across calls.
ORDER_LOG = []
TOTAL_ORDERS = 0


def process_order(data, list=[], debug=False):
    """God function: validation, pricing, logging and formatting all in one.

    Smells: shadows builtin ``list``, mutable default argument, boolean flag
    parameter, global mutation, deep nesting, bare except, magic numbers,
    string concatenation in a loop, ``== None`` comparison, unused variable.
    """
    global TOTAL_ORDERS
    temp = 42  # unused variable
    result = ""
    if data != None:
        if "items" in data:
            if len(data["items"]) > 0:
                for item in data["items"]:
                    if item.get("qty") != None:
                        if item["qty"] > 0:
                            try:
                                price = float(item["price"])
                            except:
                                price = 0
                            if price > 1000:
                                price = price * 0.9
                            elif price > 500:
                                price = price * 0.95
                            list.append(price * item["qty"])
                            result = result + item["name"] + ":" + str(round(price * item["qty"], 2)) + ";"
    TOTAL_ORDERS = TOTAL_ORDERS + 1
    ORDER_LOG.append(result)
    if debug:
        print("DEBUG " + result)
    return result


def format_us_address(name, street, city, state, zip_code):
    # Smell: duplicated code (near-identical to format_ca_address) + data clump.
    line = ""
    line = line + name.strip().title() + "\n"
    line = line + street.strip().title() + "\n"
    line = line + city.strip().title() + ", " + state.strip().upper() + " " + zip_code.strip()
    return line


def format_ca_address(name, street, city, province, postal_code):
    # Smell: duplicated code (near-identical to format_us_address) + data clump.
    line = ""
    line = line + name.strip().title() + "\n"
    line = line + street.strip().title() + "\n"
    line = line + city.strip().title() + ", " + province.strip().upper() + " " + postal_code.strip().upper()
    return line


def shipping_label(customer):
    # Smell: feature envy - only uses another object's data.
    return (
        customer["first_name"] + " " + customer["last_name"] + " | "
        + customer["address"]["city"] + " | "
        + customer["address"]["country"]
    )


def get_status_text(code):
    # Smell: switch-like if/elif chain on a primitive code; type check via type().
    if type(code) == str:
        code = int(code)
    if code == 1:
        return "PENDING"
    elif code == 2:
        return "PAID"
    elif code == 3:
        return "SHIPPED"
    elif code == 4:
        return "DELIVERED"
    elif code == 5:
        return "CANCELLED"
    else:
        return "UNKNOWN"


def old_discount_formula(subtotal):
    # Smell: dead code - never called anywhere.
    return subtotal * 0.07


class OrderManager:
    """Smell: god class / large class with unrelated responsibilities."""

    def __init__(self):
        self.orders = []
        self.emails_sent = 0
        self.report = ""

    def add(self, o):
        self.orders.append(o)

    def total(self):
        t = 0
        for i in range(len(self.orders)):  # Smell: range(len()) loop
            t = t + self.orders[i]["amount"]
        return t

    def send_email(self, to):
        # Smell: unrelated responsibility (notifications) in an order class.
        self.emails_sent = self.emails_sent + 1
        return "Sent to " + to

    def build_report(self):
        # Smell: unrelated responsibility (reporting) + string building in loop.
        self.report = ""
        for o in self.orders:
            self.report = self.report + str(o["id"]) + "=" + str(o["amount"]) + "\n"
        return self.report


def test_process_order_smelly_but_correct():
    out = process_order(
        {"items": [
            {"name": "pen", "price": "2.5", "qty": 4},
            {"name": "tv", "price": "1200", "qty": 1},
            {"name": "bad", "price": "oops", "qty": 1},
            {"name": "skip", "price": "9", "qty": 0},
        ]},
        list=[],
    )
    assert out == "pen:10.0;tv:1080.0;bad:0;"
    assert process_order(None, list=[]) == ""


def test_address_formatters():
    assert format_us_address(" jane doe ", "1 main st", "austin", "tx", "73301") == (
        "Jane Doe\n1 Main St\nAustin, TX 73301"
    )
    assert format_ca_address("john roe", "2 king st", "toronto", "on", "m5v 2t6") == (
        "John Roe\n2 King St\nToronto, ON M5V 2T6"
    )


def test_shipping_label():
    customer = {
        "first_name": "Ann",
        "last_name": "Lee",
        "address": {"city": "Boston", "country": "US"},
    }
    assert shipping_label(customer) == "Ann Lee | Boston | US"


@pytest.mark.parametrize(
    ("code", "expected"),
    [(1, "PENDING"), ("3", "SHIPPED"), (5, "CANCELLED"), (9, "UNKNOWN")],
)
def test_get_status_text(code, expected):
    assert get_status_text(code) == expected


def test_order_manager():
    m = OrderManager()
    m.add({"id": 1, "amount": 10})
    m.add({"id": 2, "amount": 15})
    assert m.total() == 25
    assert m.send_email("a@example.com") == "Sent to a@example.com"
    assert m.build_report() == "1=10\n2=15\n"


def test_calculate_loyalty_points():
    assert calculate_loyalty_points(150) == 30
    assert calculate_loyalty_points(50) == 5

from test_support import load_homework

hw = load_homework(__file__)

ROWS = [
    {"order_id": "o1", "line_id": 1, "date": "2026-01-01", "customer_id": "c1", "customer_name": "Ada", "product_id": "p1", "product_name": "Book", "qty": 2, "unit_price": 10},
    {"order_id": "o1", "line_id": 2, "date": "2026-01-01", "customer_id": "c1", "customer_name": "Ada", "product_id": "p2", "product_name": "Pen", "qty": 1, "unit_price": 3},
    {"order_id": "o2", "line_id": 1, "date": "2026-01-02", "customer_id": None, "customer_name": None, "product_id": "p1", "product_name": "Book", "qty": 1, "unit_price": 10},
]


def test_grain_dimensions_and_measures():
    model = hw.build_star_schema(ROWS)
    assert len(model["fact_order_line"]) == 3
    assert len(model["dim_product"]) == 2
    assert len(model["dim_date"]) == 2
    assert sum(r["line_revenue"] for r in model["fact_order_line"]) == 33
    assert all("customer_name" not in r and "product_name" not in r for r in model["fact_order_line"])


def test_unknown_customer_and_determinism():
    one = hw.build_star_schema(ROWS)
    two = hw.build_star_schema(list(reversed(ROWS)))
    unknown = [r for r in one["dim_customer"] if r["customer_id"] is None]
    assert len(unknown) == 1
    assert sorted(one["fact_order_line"], key=lambda x: (x["order_id"], x["line_id"])) == sorted(two["fact_order_line"], key=lambda x: (x["order_id"], x["line_id"]))

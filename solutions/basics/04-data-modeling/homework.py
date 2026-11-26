from __future__ import annotations


def build_star_schema(order_lines: list[dict]) -> dict:
    customers_by_id = {None: "Unknown"}
    products_by_id = {}
    seen_grain = set()
    for row in order_lines:
        grain = (row["order_id"], row["line_id"])
        if grain in seen_grain:
            raise ValueError(f"duplicate fact grain: {grain}")
        seen_grain.add(grain)

        customer_id = row.get("customer_id")
        customer_name = row.get("customer_name") or "Unknown"
        if customer_id is None:
            customer_name = "Unknown"
        if customer_id in customers_by_id and customers_by_id[customer_id] != customer_name:
            raise ValueError(f"conflicting attributes for customer {customer_id}")
        customers_by_id[customer_id] = customer_name

        product_id, product_name = row["product_id"], row["product_name"]
        if product_id in products_by_id and products_by_id[product_id] != product_name:
            raise ValueError(f"conflicting attributes for product {product_id}")
        products_by_id[product_id] = product_name

    customer_values = set(customers_by_id.items())
    product_values = set(products_by_id.items())
    dates = {row["date"] for row in order_lines}

    customers = sorted(customer_values, key=lambda value: (value[0] is not None, value[0] or ""))
    products = sorted(product_values)
    ordered_dates = sorted(dates)

    customer_keys = {value[0]: index for index, value in enumerate(customers)}
    product_keys = {value[0]: index + 1 for index, value in enumerate(products)}
    date_keys = {value: index + 1 for index, value in enumerate(ordered_dates)}

    dim_customer = [
        {"customer_sk": customer_keys[customer_id], "customer_id": customer_id, "customer_name": name}
        for customer_id, name in customers
    ]
    dim_product = [
        {"product_sk": product_keys[product_id], "product_id": product_id, "product_name": name}
        for product_id, name in products
    ]
    dim_date = [{"date_sk": date_keys[value], "date": value} for value in ordered_dates]

    facts = []
    for row in order_lines:
        facts.append(
            {
                "order_id": row["order_id"],
                "line_id": row["line_id"],
                "date_sk": date_keys[row["date"]],
                "customer_sk": customer_keys[row.get("customer_id")],
                "product_sk": product_keys[row["product_id"]],
                "qty": row["qty"],
                "unit_price": row["unit_price"],
                "line_revenue": row["qty"] * row["unit_price"],
            }
        )

    return {
        "fact_order_line": sorted(facts, key=lambda row: (row["order_id"], row["line_id"])),
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_date": dim_date,
    }

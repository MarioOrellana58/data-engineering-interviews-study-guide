from __future__ import annotations


def build_star_schema(order_lines: list[dict]) -> dict:
    customer_values = {(row.get("customer_id"), row.get("customer_name")) for row in order_lines}
    product_values = {(row["product_id"], row["product_name"]) for row in order_lines}
    dates = {row["date"] for row in order_lines}

    customers = sorted(customer_values, key=lambda value: (value[0] is not None, value[0] or ""))
    products = sorted(product_values)
    ordered_dates = sorted(dates)

    customer_keys = {value[0]: index for index, value in enumerate(customers)}
    product_keys = {value[0]: index + 1 for index, value in enumerate(products)}
    date_keys = {value: index + 1 for index, value in enumerate(ordered_dates)}

    dim_customer = [
        {"customer_sk": customer_keys[customer_id], "customer_id": customer_id, "customer_name": name or "Unknown"}
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

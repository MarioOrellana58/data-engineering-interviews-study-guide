WITH ranked_events AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC, ingested_at DESC, source_event_id DESC
        ) AS version_rank
    FROM order_events
),
current_paid_orders AS (
    SELECT order_id, customer_id, amount, order_at
    FROM ranked_events
    WHERE version_rank = 1 AND status = 'paid'
),
customer_metrics AS (
    SELECT
        c.customer_id,
        COUNT(o.order_id) AS order_count,
        COALESCE(SUM(o.amount), 0) AS gross_revenue,
        MAX(o.order_at) AS last_order_at
    FROM customers AS c
    LEFT JOIN current_paid_orders AS o USING (customer_id)
    GROUP BY c.customer_id
)
SELECT
    customer_id,
    order_count,
    gross_revenue,
    last_order_at,
    DENSE_RANK() OVER (ORDER BY gross_revenue DESC) AS revenue_rank
FROM customer_metrics
ORDER BY customer_id;

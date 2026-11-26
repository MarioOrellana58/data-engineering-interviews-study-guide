WITH deduplicated AS (
    SELECT * EXCLUDE (dedupe_rank)
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY event_id
                ORDER BY ingested_at DESC, event_at DESC
            ) AS dedupe_rank
        FROM events
    )
    WHERE dedupe_rank = 1
),
with_boundaries AS (
    SELECT
        *,
        CASE
            WHEN LAG(event_at) OVER (PARTITION BY user_id ORDER BY event_at, event_id) IS NULL THEN 1
            WHEN event_at - LAG(event_at) OVER (PARTITION BY user_id ORDER BY event_at, event_id) > INTERVAL '30 minutes' THEN 1
            ELSE 0
        END AS begins_session
    FROM deduplicated
),
session_events AS (
    SELECT
        *,
        SUM(begins_session) OVER (
            PARTITION BY user_id ORDER BY event_at, event_id ROWS UNBOUNDED PRECEDING
        ) AS session_number
    FROM with_boundaries
),
session_summary AS (
    SELECT
        user_id,
        session_number,
        MIN(event_at) AS session_start,
        MAX(event_at) AS session_end,
        COUNT(*) AS event_count,
        MIN(event_at) FILTER (WHERE event_name = 'view') AS first_view
    FROM session_events
    GROUP BY user_id, session_number
),
funnel_add AS (
    SELECT
        summary.*,
        MIN(event.event_at) FILTER (
            WHERE event.event_name = 'add_to_cart' AND event.event_at >= summary.first_view
        ) AS first_add
    FROM session_summary AS summary
    JOIN session_events AS event USING (user_id, session_number)
    GROUP BY ALL
),
funnel_purchase AS (
    SELECT
        stage.*,
        MIN(event.event_at) FILTER (
            WHERE event.event_name = 'purchase' AND event.event_at >= stage.first_add
        ) AS first_purchase
    FROM funnel_add AS stage
    JOIN session_events AS event USING (user_id, session_number)
    GROUP BY ALL
)
SELECT
    user_id,
    session_number,
    session_start,
    session_end,
    event_count,
    first_purchase IS NOT NULL AS completed_funnel,
    CASE WHEN first_purchase IS NOT NULL THEN DATE_DIFF('second', first_view, first_purchase) END AS seconds_to_purchase
FROM funnel_purchase
ORDER BY user_id, session_number;

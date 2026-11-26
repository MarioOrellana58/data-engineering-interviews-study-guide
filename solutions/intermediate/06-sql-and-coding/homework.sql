WITH deduplicated AS (
    SELECT * EXCLUDE (dedupe_rank)
    FROM (
        SELECT *, ROW_NUMBER() OVER (
            PARTITION BY event_id
            ORDER BY ingested_at DESC, event_at DESC, event_name DESC, user_id DESC
        ) AS dedupe_rank
        FROM events
    )
    WHERE dedupe_rank = 1
),
with_boundaries AS (
    SELECT *, CASE
        WHEN LAG(event_at) OVER (PARTITION BY user_id ORDER BY event_at, event_id) IS NULL THEN 1
        WHEN event_at - LAG(event_at) OVER (PARTITION BY user_id ORDER BY event_at, event_id) > INTERVAL '30 minutes' THEN 1
        ELSE 0
    END AS begins_session
    FROM deduplicated
),
session_events AS (
    SELECT *, SUM(begins_session) OVER (
        PARTITION BY user_id ORDER BY event_at, event_id ROWS UNBOUNDED PRECEDING
    ) AS session_number
    FROM with_boundaries
),
positioned AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY user_id, session_number ORDER BY event_at, event_id
    ) AS event_position
    FROM session_events
),
session_summary AS (
    SELECT user_id, session_number, MIN(event_at) AS session_start,
           MAX(event_at) AS session_end, COUNT(*) AS event_count,
           MIN(event_position) FILTER (WHERE event_name = 'view') AS first_view_position
    FROM positioned
    GROUP BY user_id, session_number
),
funnel_add AS (
    SELECT summary.*, MIN(event.event_position) FILTER (
        WHERE event.event_name = 'add_to_cart' AND event.event_position > summary.first_view_position
    ) AS first_add_position
    FROM session_summary AS summary
    JOIN positioned AS event USING (user_id, session_number)
    GROUP BY ALL
),
funnel_purchase AS (
    SELECT stage.*, MIN(event.event_position) FILTER (
        WHERE event.event_name = 'purchase' AND event.event_position > stage.first_add_position
    ) AS first_purchase_position
    FROM funnel_add AS stage
    JOIN positioned AS event USING (user_id, session_number)
    GROUP BY ALL
)
SELECT stage.user_id, stage.session_number, stage.session_start, stage.session_end,
       stage.event_count, purchase.event_position IS NOT NULL AS completed_funnel,
       CASE WHEN purchase.event_position IS NOT NULL
            THEN DATE_DIFF('second', view_event.event_at, purchase.event_at) END AS seconds_to_purchase
FROM funnel_purchase AS stage
LEFT JOIN positioned AS view_event
  ON view_event.user_id = stage.user_id AND view_event.session_number = stage.session_number
 AND view_event.event_position = stage.first_view_position
LEFT JOIN positioned AS purchase
  ON purchase.user_id = stage.user_id AND purchase.session_number = stage.session_number
 AND purchase.event_position = stage.first_purchase_position
ORDER BY stage.user_id, stage.session_number;

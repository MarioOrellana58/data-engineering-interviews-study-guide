import duckdb

from test_support import homework_path


def run_query():
    con = duckdb.connect()
    con.execute("CREATE TABLE customers(customer_id VARCHAR); INSERT INTO customers VALUES ('c1'), ('c2'), ('c3')")
    con.execute("""CREATE TABLE order_events(source_event_id VARCHAR, order_id VARCHAR, customer_id VARCHAR, status VARCHAR, amount DECIMAL(10,2), order_at TIMESTAMP, updated_at TIMESTAMP, ingested_at TIMESTAMP)""")
    con.execute("""INSERT INTO order_events VALUES
      ('v1','o1','c1','paid',10,'2026-01-01','2026-01-01 10:00','2026-01-01 10:01'),
      ('v2','o1','c1','paid',12,'2026-01-01','2026-01-01 11:00','2026-01-01 11:01'),
      ('v3','o2','c1','paid',8,'2026-01-03','2026-01-03 10:00','2026-01-03 10:01'),
      ('v4','o2','c1','cancelled',8,'2026-01-03','2026-01-03 11:00','2026-01-03 11:01'),
      ('v5','o3','c2','paid',12,'2026-01-02','2026-01-02 10:00','2026-01-02 10:01'),
      ('v6','o3','c2','paid',15,'2026-01-02','2026-01-02 10:00','2026-01-02 10:01')""")
    sql = homework_path(__file__, "homework.sql").read_text(encoding="utf-8")
    return con.execute(sql).fetchall(), [d[0] for d in con.description]


def test_customer_metrics_and_ties():
    rows, columns = run_query()
    assert columns == ["customer_id", "order_count", "gross_revenue", "last_order_at", "revenue_rank"]
    by_id = {r[0]: r for r in rows}
    assert set(by_id) == {"c1", "c2", "c3"}
    assert by_id["c1"][1:3] == (1, 12)
    assert by_id["c2"][1:3] == (1, 15)
    assert by_id["c2"][4] == 1 and by_id["c1"][4] == 2
    assert by_id["c3"][1] == 0 and by_id["c3"][2] == 0

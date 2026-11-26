import duckdb

from test_support import homework_path


def test_sessionization_and_ordered_funnel():
    con = duckdb.connect()
    con.execute("CREATE TABLE events(event_id VARCHAR,user_id VARCHAR,event_name VARCHAR,event_at TIMESTAMP,ingested_at TIMESTAMP)")
    con.execute("""INSERT INTO events VALUES
      ('1','u1','view','2026-01-01 10:00','2026-01-01 10:01'),
      ('2','u1','add_to_cart','2026-01-01 10:05','2026-01-01 10:06'),
      ('3','u1','purchase','2026-01-01 10:10','2026-01-01 10:11'),
      ('3','u1','purchase','2026-01-01 10:10','2026-01-01 10:12'),
      ('4','u1','view','2026-01-01 10:41','2026-01-01 10:41'),
      ('5','u1','purchase','2026-01-01 10:42','2026-01-01 10:42'),
      ('6','u2','purchase','2026-01-01 09:00','2026-01-01 09:01'),
      ('7','u2','view','2026-01-01 09:01','2026-01-01 09:02')""")
    sql = homework_path(__file__, "homework.sql").read_text(encoding="utf-8")
    rows = con.execute(sql).fetchall()
    columns = [x[0] for x in con.description]
    assert columns == ["user_id", "session_number", "session_start", "session_end", "event_count", "completed_funnel", "seconds_to_purchase"]
    by_key = {(r[0], r[1]): r for r in rows}
    assert len(by_key) == 3
    assert by_key[("u1", 1)][4:] == (3, True, 600)
    assert by_key[("u1", 2)][4] == 2 and by_key[("u1", 2)][5] is False
    assert by_key[("u2", 1)][5] is False


def test_equal_timestamps_use_event_id_as_the_ordering_tiebreaker():
    con = duckdb.connect()
    con.execute("CREATE TABLE events(event_id VARCHAR,user_id VARCHAR,event_name VARCHAR,event_at TIMESTAMP,ingested_at TIMESTAMP)")
    con.execute("""INSERT INTO events VALUES
      ('1','u','purchase','2026-01-01 10:00','2026-01-01 10:01'),
      ('2','u','add_to_cart','2026-01-01 10:00','2026-01-01 10:01'),
      ('3','u','view','2026-01-01 10:00','2026-01-01 10:01')""")
    sql = homework_path(__file__, "homework.sql").read_text(encoding="utf-8")
    row = con.execute(sql).fetchone()
    assert row[5] is False

SCHEMA = [
    """DROP TABLE IF EXISTS listening_events""",
    """DROP TABLE IF EXISTS listens""",
    """DROP TABLE IF EXISTS media""",
    """CREATE TABLE listening_events (
          timestamp INTEGER,
          ms_played INTEGER,
          media_format TEXT,
          media_type TEXT,
          media_uri TEXT,
          media_title TEXT,
          media_creator TEXT,
          reason_start TEXT,
          reason_end TEXT,
          shuffle INTEGER,
          skipped INTEGER,
          offline INTEGER,
          conn_country TEXT
        )""",
    """CREATE TABLE listens (
        timestamp INTEGER,
        ms_played INTEGER,
        media_uri TEXT,
        media_format TEXT,
        reason_start TEXT,
        reason_end TEXT,
        shuffle INTEGER,
        skipped INTEGER,
        offline INTEGER,
        conn_country TEXT
    )""",
    """CREATE TABLE media (
        media_uri TEXT,
        media_type TEXT,
        media_title TEXT,
        media_creator TEXT
    )""",
]

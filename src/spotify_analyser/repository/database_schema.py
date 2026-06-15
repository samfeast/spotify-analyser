SCHEMA = ["""CREATE TABLE IF NOT EXISTS listening_events (
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
          )"""]

from collections.abc import Iterator
from dataclasses import astuple
import logging
import sqlite3

from spotify_analyser.repository.listening_event import ListeningEvent

logger = logging.getLogger(__name__)


class DataRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_listening_history(
        self, events: Iterator[ListeningEvent], limit: int, batch_size: int = 1000
    ) -> None:
        logger.info(
            (
                f"Inserting {f'up to {limit}' if limit >= 0 else ''}"
                f"listening events with batch size {batch_size}"
            )
        )
        self.__insert_raw_listening_events(events, limit, batch_size)
        self.__insert_media()
        self.__insert_listens()
        self.__drop_raw_listening_events()

    def __insert_raw_listening_events(
        self, events: Iterator[ListeningEvent], limit: int, batch_size: int
    ) -> None:
        cur = self.conn.cursor()

        batch: list[ListeningEvent] = []
        inserted = 0

        for event in events:
            if limit >= 0 and inserted >= limit:
                logger.warning(
                    "Listening event limit reached, not all events have been stored"
                )
                break

            batch.append(event)
            inserted += 1

            if len(batch) >= batch_size:
                self.__insert_listening_event_batch(cur, batch)
                batch.clear()

        if batch:
            self.__insert_listening_event_batch(cur, batch)

        logger.info(f"Finished inserting {inserted} listening events")

    def __insert_listening_event_batch(
        self, cur: sqlite3.Cursor, batch: list[ListeningEvent]
    ) -> None:
        logger.debug(f"Inserting batch of {len(batch)} listening events")
        cur.executemany(
            """
            INSERT INTO listening_events (
                timestamp,
                ms_played,
                media_format,
                media_type,
                media_uri,
                media_title,
                media_creator,
                reason_start,
                reason_end,
                shuffle,
                skipped,
                offline,
                conn_country
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [astuple(event) for event in batch],
        )

    def __insert_media(self) -> None:
        cur = self.conn.cursor()

        logger.info("Inserting distinct tracks and episodes into media table")

        cur.execute(
            """
            WITH variants AS (
                SELECT
                    media_uri,
                    media_type,
                    media_creator,
                    media_title,
                    COUNT(*) AS occurrences
                FROM listening_events
                GROUP BY
                    media_uri,
                    media_type,
                    media_title,
                    media_creator
            ),
            ranked AS (
                SELECT
                    *,
                    ROW_NUMBER() OVER (
                        PARTITION BY media_uri
                        ORDER BY occurrences DESC
                    ) AS rn
                FROM variants
            )
            INSERT INTO media (
                media_uri,
                media_type,
                media_title,
                media_creator
            )
            SELECT
                media_uri,
                media_type,
                media_title,
                media_creator
            FROM ranked
            WHERE rn = 1
            """,
        )

    def __insert_listens(self) -> None:
        cur = self.conn.cursor()

        logger.info("Inserting listening data into listens table")

        cur.execute(
            """
            INSERT INTO listens (
                timestamp,
                ms_played,
                media_uri,
                media_format,
                reason_start,
                reason_end,
                shuffle,
                skipped,
                offline,
                conn_country
            )
            SELECT
                timestamp,
                ms_played,
                media_uri,
                media_format,
                reason_start,
                reason_end,
                shuffle,
                skipped,
                offline,
                conn_country
            FROM listening_events
            """,
        )

    def __drop_raw_listening_events(self) -> None:
        cur = self.conn.cursor()
        logger.info("Dropping listening_events table")
        cur.execute("DROP TABLE IF EXISTS listening_events")

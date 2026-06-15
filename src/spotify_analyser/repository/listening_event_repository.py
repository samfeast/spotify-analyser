from collections.abc import Iterator
from dataclasses import astuple
import logging
import sqlite3

from spotify_analyser.repository.listening_event import ListeningEvent

logger = logging.getLogger(__name__)


class ListeningEventRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_listening_events(
        self, events: Iterator[ListeningEvent], limit: int, batch_size: int = 1000
    ) -> None:
        logger.info(
            (
                f"Inserting {f'up to {limit}' if limit >= 0 else ''}"
                f"listening events with batch size {batch_size}"
            )
        )

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
                self.__insert_listening_event_batch(batch)
                batch.clear()

        if batch:
            self.__insert_listening_event_batch(batch)

        logger.info(f"Finished inserting {inserted} listening events")

    def __insert_listening_event_batch(self, batch: list[ListeningEvent]) -> None:
        logger.debug(f"Inserting batch of {len(batch)} listening events")
        self.conn.executemany(
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

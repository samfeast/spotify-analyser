from collections.abc import Iterator
import sqlite3

from spotify_analyser.repository.listening_event import ListeningEvent


class ListeningEventRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_listening_events(
        self, events: Iterator[ListeningEvent], limit: int, batch_size: int = 1000
    ) -> None:
        batch: list[ListeningEvent] = []
        inserted = 0

        for event in events:
            if limit >= 0 and inserted >= limit:
                break

            batch.append(event)
            inserted += 1

            if len(batch) >= batch_size:
                self.__insert_listening_event_batch(batch)
                batch.clear()

        if batch:
            self.__insert_listening_event_batch(batch)

    def __insert_listening_event_batch(self, batch: list[ListeningEvent]) -> None:
        self.conn.executemany(
            """INSERT INTO listening_events VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    event.timestamp,
                    event.ms_played,
                    event.media_format,
                    event.media_type,
                    event.media_uri,
                    event.media_title,
                    event.media_creator,
                )
                for event in batch
            ],
        )

from collections.abc import Iterator
import sqlite3

from spotify_analyser.repository.listening_event import ListeningEvent


class ListeningEventRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_listening_events(
        self, events: Iterator[ListeningEvent], batch_size: int = 1000
    ) -> None:
        batch: list[ListeningEvent] = []
        for event in events:
            batch.append(event)

            if len(batch) >= batch_size:
                self.__insert_listening_event_batch(batch)
                batch.clear()

        if batch:
            self.__insert_listening_event_batch(batch)

    def __insert_listening_event_batch(self, batch: list[ListeningEvent]) -> None:
        # TODO: insert batch (sql query)
        print(f"Adding batch of {len(batch)}")
        print(batch[0])
        pass

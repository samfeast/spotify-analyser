from pathlib import Path
import sqlite3

from spotify_analyser.repository.database_schema import SCHEMA


class DatabaseConnection:
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.__try_initialise_database()

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.conn.close()

    def __try_initialise_database(self) -> None:
        try:
            cursor = self.conn.cursor()
            for statement in SCHEMA:
                cursor.execute(statement)

        except sqlite3.OperationalError as e:
            print(f"Failed to create tables: {e}")

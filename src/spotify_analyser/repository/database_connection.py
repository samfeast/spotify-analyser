from pathlib import Path
import sqlite3


class DatabaseConnection:
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.conn.close()

import logging
from pathlib import Path
import sqlite3

from spotify_analyser.repository.database_schema import SCHEMA

logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        logger.debug("Databse connection established")
        self.__initialise_database()
        logger.debug("Database initialised with schema")

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            logger.error(
                "Database connection exited with exception, rolling back changes",
                exc_info=True,
            )
            self.conn.rollback()

        self.conn.close()

    def __initialise_database(self) -> None:
        try:
            cursor = self.conn.cursor()
            for statement in SCHEMA:
                cursor.execute(statement)

        except sqlite3.OperationalError as e:
            logger.exception(f"Failed to initialise database: {e}")

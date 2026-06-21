import logging

from spotify_analyser.ingest.data_loader import DataLoader
from spotify_analyser.repository.data_repository import DataRepository

logger = logging.getLogger(__name__)


class SpotifyAnalyserApp:
    def __init__(self, loader: DataLoader, repository: DataRepository):
        self.loader = loader
        self.repository = repository

    def ingest(self, limit: int = -1) -> None:
        logger.info(
            f"Ingesting {limit if limit >= 0 else "all"} listening events from data files"
        )
        event_iterator = self.loader.load_data()
        self.repository.insert_listening_history(event_iterator, limit)

import logging

from spotify_analyser.ingest.data_loader import DataLoader
from spotify_analyser.repository.listening_event_repository import (
    ListeningEventRepository,
)

logger = logging.getLogger(__name__)


class SpotifyAnalyserApp:
    def __init__(self, loader: DataLoader, repository: ListeningEventRepository):
        self.loader = loader
        self.repository = repository

    def ingest(self, limit: int = -1) -> None:
        logger.info(
            f"Ingesting {limit if limit >= 0 else "all"} listening events from data files"
        )
        event_iterator = self.loader.load_data()
        self.repository.insert_listening_events(event_iterator, limit)

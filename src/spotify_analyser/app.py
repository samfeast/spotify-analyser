from spotify_analyser.ingest.data_loader import DataLoader
from spotify_analyser.repository.listening_event_repository import (
    ListeningEventRepository,
)


class SpotifyAnalyserApp:
    def __init__(self, loader: DataLoader, repository: ListeningEventRepository):
        self.loader = loader
        self.repository = repository

    def ingest(self) -> None:
        event_iterator = self.loader.load_data()
        self.repository.insert_listening_events(event_iterator)

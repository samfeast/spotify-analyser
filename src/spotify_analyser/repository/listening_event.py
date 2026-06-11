from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListeningEvent:
    timestamp: int
    ms_played: int
    media_format: str
    media_type: str
    media_uri: str
    media_title: str
    media_creator: str

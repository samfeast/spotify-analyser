from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class ListeningEvent:
    event_type: EventType
    ms_played: int


class EventType(Enum):
    VIDEO = 0
    AUDIO = 1

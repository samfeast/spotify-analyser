from collections.abc import Iterator
from pathlib import Path
import ijson

from spotify_analyser.repository.listening_event import ListeningEvent, EventType


class DataLoader:
    def __init__(self, data_files: list[Path]):
        self.data_files = data_files

    def load_data(self) -> Iterator[ListeningEvent]:
        for path in self.data_files:
            yield from self.__parse_file(path)

    def __parse_file(self, path: Path) -> Iterator[ListeningEvent]:
        with open(path, "r") as read_file:
            file_name = path.name.lower()

            if "audio" in file_name:
                yield from self.__parse_audio_events(read_file)
            elif "video" in file_name:
                yield from self.__parse_video_events(read_file)
            else:
                raise NotImplementedError(
                    "Automatic type detection is not implemented."
                )

    def __parse_audio_events(self, file) -> Iterator[ListeningEvent]:
        for item in ijson.items(file, "item"):
            if item["ms_played"] == 0:
                continue

            yield ListeningEvent(EventType.AUDIO, item["ms_played"])

    def __parse_video_events(self, file) -> Iterator[ListeningEvent]:
        for item in ijson.items(file, "item"):
            if item["ms_played"] == 0:
                continue

            yield ListeningEvent(EventType.VIDEO, item["ms_played"])

from collections.abc import Iterator
from datetime import datetime
import logging
from pathlib import Path
import ijson

from spotify_analyser.repository.listening_event import ListeningEvent

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, data_files: list[Path]):
        self.data_files = data_files

    def load_data(self) -> Iterator[ListeningEvent]:
        logger.info(f"Attempting to load data from {len(self.data_files)} data files")
        for path in self.data_files:
            yield from self.__parse_file(path)

    def __parse_file(self, path: Path) -> Iterator[ListeningEvent]:
        with open(path, "r") as read_file:
            logger.info(f"Parsing events from {path.name}")
            file_name = path.name.lower()

            if "audio" in file_name:
                yield from self.__parse_events(read_file, "audio")
            elif "video" in file_name:
                yield from self.__parse_events(read_file, "video")
            else:
                logger.warning(
                    "File name does not contain audio or video, media format is unknown"
                )
                yield from self.__parse_events(read_file, "unknown")

    def __parse_events(self, file, media_format: str) -> Iterator[ListeningEvent]:
        for item in ijson.items(file, "item"):
            if item["ms_played"] == 0:
                continue

            timestamp = int(
                datetime.fromisoformat(item["ts"].replace("Z", "+00:00")).timestamp()
            )

            if (
                item["spotify_track_uri"] is not None
                and item["spotify_episode_uri"] is None
            ):
                yield ListeningEvent(
                    timestamp,
                    item["ms_played"],
                    media_format,
                    "track",
                    item["spotify_track_uri"],
                    item["master_metadata_track_name"],
                    item["master_metadata_album_artist_name"],
                )
            elif (
                item["spotify_episode_uri"] is not None
                and item["spotify_track_uri"] is None
            ):
                yield ListeningEvent(
                    timestamp,
                    item["ms_played"],
                    media_format,
                    "episode",
                    item["spotify_episode_uri"],
                    item["episode_name"],
                    item["episode_show_name"],
                )
            else:
                logger.warning(
                    f"Failed to parse event: incorrect number of uri's present\n{item}"
                )

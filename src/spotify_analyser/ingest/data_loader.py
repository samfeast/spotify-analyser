from collections.abc import Iterator
from datetime import datetime
import logging
from pathlib import Path
from typing import TextIO
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

    def __parse_events(
        self, file: TextIO, media_format: str
    ) -> Iterator[ListeningEvent]:
        for item in ijson.items(file, "item"):
            try:
                event = self.__parse_event(item, media_format)
                if event is None:
                    continue
                else:
                    yield event
            except KeyError:
                logger.warning(f"Failed to parse event, missing fields: {item}")

    def __parse_event(
        self, item: ijson.items, media_format: str
    ) -> ListeningEvent | None:
        ms_played = item["ms_played"]
        if ms_played == 0:
            return None

        timestamp = int(
            datetime.fromisoformat(item["ts"].replace("Z", "+00:00")).timestamp()
        )

        track_uri = item["spotify_track_uri"]
        episode_uri = item["spotify_episode_uri"]

        if track_uri is not None and episode_uri is None:
            media_type = "track"
            media_uri = track_uri
            media_title = item["master_metadata_track_name"]
            media_creator = item["master_metadata_album_artist_name"]
        elif episode_uri is not None and track_uri is None:
            media_type = "episode"
            media_uri = episode_uri
            media_title = item["episode_name"]
            media_creator = item["episode_show_name"]
        else:
            logger.warning(
                f"Failed to parse event, incorrect number of uri's present: {item}"
            )
            return None

        return ListeningEvent(
            timestamp,
            ms_played,
            media_format,
            media_type,
            media_uri,
            media_title,
            media_creator,
            item["reason_start"],
            item["reason_end"],
            item["shuffle"],
            item["skipped"],
            item["offline"],
            item["conn_country"],
        )

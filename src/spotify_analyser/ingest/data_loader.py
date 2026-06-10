from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
import ijson

from spotify_analyser.config import DEFAULT_DATA_PATH

BATCH_SIZE = 1000


class DataLoader:
    def __init__(self, input_path: Path | None = None):
        self.data_path = self.get_data_path(input_path)
        self.data_files: list[Path] = []

    # Get valid Path to use as data directory
    def get_data_path(self, input_path: Path | None = None) -> Path:
        if input_path is None:
            return DEFAULT_DATA_PATH

        abs_path = input_path.expanduser().resolve()
        if abs_path.exists() and abs_path.is_dir():
            return abs_path

        raise NotADirectoryError(f"{input_path} does not exist or is not a directory.")

    def select_data_files(self) -> None:
        print("Select which data is parsed:\n\t(1) Select all\n\t(2) Custom selection")

        while True:
            user_input = input("Input: ")

            if user_input == "1":
                self.data_files = self.__get_all_data_files()
                return

            if user_input == "2":
                self.data_files = self.__get_custom_data_files()
                return

            print("Invalid selection")

    def __get_all_data_files(self) -> list[Path]:
        all_files = list(self.data_path.iterdir())

        return [f for f in all_files if f.suffix == ".json"]

    def __get_custom_data_files(self) -> list[Path]:
        raise NotImplementedError

    def load_data(self) -> None:
        listening_events = self.__get_listening_event_iterator()

        batch: list[ListeningEvent] = []
        for event in listening_events:
            batch.append(event)

            if len(batch) >= BATCH_SIZE:
                self.__flush_event_batch(batch)
                batch.clear()

        if batch:
            self.__flush_event_batch(batch)
            batch.clear()

    def __get_listening_event_iterator(self) -> Iterator[ListeningEvent]:
        for path in self.data_files:
            yield from self.__parse_file(path)

    def __parse_file(self, path: Path) -> Iterator[ListeningEvent]:

        with open(path, "r") as read_file:
            for item in ijson.items(read_file, "item"):
                yield ListeningEvent(item["ms_played"])

    def __flush_event_batch(self, batch: list[ListeningEvent]) -> None:
        # TODO: Write batch to SQLite DB
        pass


# TODO: Add fields
@dataclass(frozen=True, slots=True)
class ListeningEvent:
    ms_played: int

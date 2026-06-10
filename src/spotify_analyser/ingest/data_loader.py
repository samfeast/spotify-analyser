from pathlib import Path
from spotify_analyser.config import DEFAULT_DATA_PATH


class DataLoader:
    def __init__(self, input_path: Path | None = None):
        self.data_path = self.get_data_path(input_path)

    # Get valid Path to use as data directory
    def get_data_path(self, input_path: Path | None = None) -> Path:
        if input_path is None:
            return DEFAULT_DATA_PATH

        abs_path = input_path.expanduser().resolve()
        if abs_path.exists() and abs_path.is_dir():
            return abs_path

        raise NotADirectoryError(f"{input_path} does not exist or is not a directory.")

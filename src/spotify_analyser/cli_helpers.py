import logging
from pathlib import Path
import argparse

from spotify_analyser.config import DEFAULT_DATA_DIR

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        default=DEFAULT_DATA_DIR,
        type=Path,
        help="Specify path to data directory",
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging verbosity",
    )

    parser.add_argument(
        "--console-log", action="store_true", help="Also print log messages to stderr"
    )

    return parser.parse_args()


def validate_data_path(input_path: Path) -> Path:
    abs_path = input_path.expanduser().resolve()
    if abs_path.exists() and abs_path.is_dir():
        return abs_path

    raise NotADirectoryError(f"{input_path} does not exist or is not a directory.")


def select_data_files(data_dir: Path) -> list[Path]:
    print("Select which data is parsed:\n\t(1) Select all\n\t(2) Custom selection")

    while True:
        user_input = input("Input: ")

        if user_input == "1":
            return _get_all_data_files(data_dir)

        if user_input == "2":
            return _get_custom_data_files(data_dir)

        print("Invalid selection")


def _get_all_data_files(data_dir: Path) -> list[Path]:
    logger.info(f"Getting all json files in directory {data_dir}")
    return list(data_dir.glob("*.json"))


def _get_custom_data_files(data_dir: Path) -> list[Path]:
    raise NotImplementedError("Custom data selection is not implemented.")

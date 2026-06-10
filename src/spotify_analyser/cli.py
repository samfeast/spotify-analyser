from pathlib import Path
import argparse

from spotify_analyser.ingest.data_loader import DataLoader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=Path, help="Specify path to data directory")

    args = parser.parse_args()

    data_loader = DataLoader(args.data_path)


if __name__ == "__main__":
    main()

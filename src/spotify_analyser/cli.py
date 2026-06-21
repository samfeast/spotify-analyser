import logging

from spotify_analyser.app import SpotifyAnalyserApp
from spotify_analyser.cli_helpers import (
    parse_args,
    validate_data_path,
    select_data_files,
)
from spotify_analyser.config import DATABASE_PATH
from spotify_analyser.ingest.data_loader import DataLoader
from spotify_analyser.logging_config import configure_logging
from spotify_analyser.repository.database_connection import DatabaseConnection
from spotify_analyser.repository.data_repository import DataRepository

logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    configure_logging(args.log_level, args.console_log)

    print(args.data_dir)

    data_dir = validate_data_path(args.data_dir)
    logger.info("Starting file selection dialog")
    data_files = select_data_files(data_dir)

    with DatabaseConnection(DATABASE_PATH) as conn:
        logger.debug("Instantiating loader and repository")
        loader = DataLoader(data_files)
        repository = DataRepository(conn)

        logger.info("Starting spotify analyser app")
        app = SpotifyAnalyserApp(loader, repository)

        app.ingest()


if __name__ == "__main__":
    main()

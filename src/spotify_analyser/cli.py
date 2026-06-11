from spotify_analyser.app import SpotifyAnalyserApp
from spotify_analyser.cli_helpers import (
    parse_args,
    validate_data_path,
    select_data_files,
)
from spotify_analyser.config import DATABASE_PATH
from spotify_analyser.ingest.data_loader import DataLoader
from spotify_analyser.repository.database_connection import DatabaseConnection
from spotify_analyser.repository.listening_event_repository import (
    ListeningEventRepository,
)


def main():
    args = parse_args()

    data_dir = validate_data_path(args.data_dir)
    data_files = select_data_files(data_dir)

    with DatabaseConnection(DATABASE_PATH) as conn:
        loader = DataLoader(data_files)
        repository = ListeningEventRepository(conn)

        app = SpotifyAnalyserApp(loader, repository)

        app.ingest()


if __name__ == "__main__":
    main()

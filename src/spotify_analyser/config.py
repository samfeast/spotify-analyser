from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"

DATABASE_PATH = PROJECT_ROOT / "storage" / "database.db"

LOG_FILE = PROJECT_ROOT / "logs" / "spotify_analyser.log"

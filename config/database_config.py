from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    DEFAULT_DB_PATH: str = "vocabulary.db"
    SQLITE_TIMEOUT: int = 30
    SQLITE_ISOLATION_LEVEL: str = None  # None = autocommit mode 
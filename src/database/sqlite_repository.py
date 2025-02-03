import sqlite3
import json
from typing import List, Optional, Generator
from .vocabulary_repository import VocabularyRepository
from .models import VocabularyEntry
from src.models.vocabulary_models import VocabularyEntryOutputModel
from contextlib import contextmanager
from config.database_config import DatabaseConfig
import logging

class SQLiteVocabularyRepository(VocabularyRepository):
    def __init__(self, db_path: str = DatabaseConfig.DEFAULT_DB_PATH):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vocabulary (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    learning_language TEXT NOT NULL,
                    interface_language TEXT NOT NULL,
                    word_phrase TEXT NOT NULL,
                    translation TEXT NOT NULL,
                    definitions TEXT NOT NULL,
                    example_sentence TEXT NOT NULL
                )
            """)
    
    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connections"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=DatabaseConfig.SQLITE_TIMEOUT,
            isolation_level=DatabaseConfig.SQLITE_ISOLATION_LEVEL
        )
        try:
            yield conn
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()

    def add_entry(self, entry: VocabularyEntry) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO vocabulary (
                        user_id, learning_language, interface_language,
                        word_phrase, translation, definitions, example_sentence
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry.user_id, entry.learning_language, entry.interface_language,
                    entry.word_phrase, entry.translation, json.dumps(entry.definitions),
                    entry.example_sentence
                ))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                conn.rollback()
                self.logger.error(f"Error adding entry: {str(e)}")
                raise
    
    def get_entries(self, user_id: str) -> List[VocabularyEntry]:
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vocabulary WHERE user_id = ?", (user_id,))
                return [self._row_to_entry(row) for row in cursor.fetchall()]
            except sqlite3.Error as e:
                self.logger.error(f"Error getting entries: {str(e)}")
                raise
    
    def get_entry(self, entry_id: int) -> Optional[VocabularyEntry]:
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vocabulary WHERE entry_id = ?", (entry_id,))
                row = cursor.fetchone()
                return self._row_to_entry(row) if row else None
            except sqlite3.Error as e:
                self.logger.error(f"Error getting entry: {str(e)}")
                raise
    
    def delete_entry(self, entry_id: int) -> bool:
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vocabulary WHERE entry_id = ?", (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                conn.rollback()
                self.logger.error(f"Error deleting entry: {str(e)}")
                raise
    
    def _row_to_entry(self, row) -> VocabularyEntry:
        return VocabularyEntry(
            entry_id=row[0],
            user_id=row[1],
            learning_language=row[2],
            interface_language=row[3],
            word_phrase=row[4],
            translation=row[5],
            definitions=json.loads(row[6]),
            example_sentence=row[7]
        )
    
    def get_vocabulary_for_prompt(self, user_id: str, learning_language: str) -> List[VocabularyEntryOutputModel]:
        entries = self.get_entries(user_id)
        return [
            VocabularyEntryOutputModel(
                word_phrase=entry.word_phrase,
                translation=entry.translation,
                definitions=entry.definitions,
                example=entry.example_sentence
            )
            for entry in entries
            if entry.learning_language == learning_language
        ] 
import sqlite3
import json
from typing import List, Optional
from .vocabulary_repository import VocabularyRepository
from .models import VocabularyEntry
from src.models.vocabulary_models import VocabularyEntryOutputModel

class SQLiteVocabularyRepository(VocabularyRepository):
    def __init__(self, db_path: str = "vocabulary.db"):
        self.db_path = db_path
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
    
    def add_entry(self, entry: VocabularyEntry) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
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
            return cursor.lastrowid
    
    def get_entries(self, user_id: str) -> List[VocabularyEntry]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vocabulary WHERE user_id = ?", (user_id,))
            return [self._row_to_entry(row) for row in cursor.fetchall()]
    
    def get_entry(self, entry_id: int) -> Optional[VocabularyEntry]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vocabulary WHERE entry_id = ?", (entry_id,))
            row = cursor.fetchone()
            return self._row_to_entry(row) if row else None
    
    def delete_entry(self, entry_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vocabulary WHERE entry_id = ?", (entry_id,))
            return cursor.rowcount > 0
    
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
from dataclasses import dataclass
from typing import List

@dataclass
class VocabularyEntry:
    entry_id: int
    user_id: str
    learning_language: str
    interface_language: str
    word_phrase: str
    translation: str
    definitions: List[str]
    example_sentence: str 
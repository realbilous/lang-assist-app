from abc import ABC, abstractmethod
from typing import List, Optional
from .models import VocabularyEntry
from src.models.vocabulary_models import VocabularyEntryOutputModel

class VocabularyRepository(ABC):
    @abstractmethod
    def add_entry(self, entry: VocabularyEntry) -> int:
        pass
    
    @abstractmethod
    def get_entries(self, user_id: str) -> List[VocabularyEntry]:
        pass
    
    @abstractmethod
    def get_entry(self, entry_id: int) -> Optional[VocabularyEntry]:
        pass
    
    @abstractmethod
    def delete_entry(self, entry_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_vocabulary_for_prompt(self, user_id: str, learning_language: str) -> List[VocabularyEntryOutputModel]:
        """Get vocabulary in a format suitable for prompts"""
        pass 
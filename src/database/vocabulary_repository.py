from abc import ABC, abstractmethod
from typing import List, Optional
from .models import VocabularyEntry

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
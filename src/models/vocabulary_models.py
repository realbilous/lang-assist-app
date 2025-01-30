from pydantic import BaseModel, Field
from typing import List

class VocabularyEntryOutputModel(BaseModel):
    word_phrase: str = Field(..., description="Original word or phrase")
    translation: str = Field(..., description="Primary translation of the word/phrase")
    definitions: List[str] = Field(
        ..., 
        description="List of definitions/meanings",
        max_items=3
    )
    example: str = Field(..., description="Example sentence using the word/phrase")

    def format_for_prompt(self) -> str:
        """Format vocabulary entry for prompt consumption"""
        return f"{self.word_phrase} - {self.translation}" 
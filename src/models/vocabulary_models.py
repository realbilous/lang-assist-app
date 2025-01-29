from pydantic import BaseModel, Field
from typing import List

class VocabularyAnalysis(BaseModel):
    translation: str = Field(..., description="Primary translation of the word/phrase")
    definitions: List[str] = Field(
        ..., 
        description="List of definitions/meanings",
        max_items=3
    )
    example: str = Field(..., description="Example sentence using the word/phrase") 
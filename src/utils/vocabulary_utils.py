from src.models.vocabulary_models import VocabularyAnalysis
import json
from typing import Union

def parse_vocabulary_response(response_content: str) -> Union[VocabularyAnalysis, None]:
    """
    Parse and validate the vocabulary analysis response from the LLM.
    
    Args:
        response_content (str): Raw response content from the LLM
        
    Returns:
        VocabularyAnalysis: Validated vocabulary analysis object
        
    Raises:
        ValueError: If the response cannot be parsed or validated
    """
    try:
        # Parse JSON response
        data = json.loads(response_content)
        
        # Validate and convert to Pydantic model
        return VocabularyAnalysis(**data)
        
    except json.JSONDecodeError:
        raise ValueError("Failed to parse LLM response as JSON")
    except Exception as e:
        raise ValueError(f"Invalid vocabulary analysis format: {str(e)}") 
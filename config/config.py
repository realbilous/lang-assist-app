from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class TaskConfig:
    display_name: str
    requires_vocabulary: bool = False
    instructions: Optional[str] = None

# Available languages for the application
INTERFACE_LANGUAGES = [
    "English",
    "Spanish",
    "German",
    "Polish",
    "Ukrainian",
    "Russian"
]

LEARNING_LANGUAGES = [
    "English",
    "Spanish",
    "German",
    "Polish",
    "Ukrainian",
    "Russian"
]

TASK_OPTIONS: Dict[str, TaskConfig] = {
    "Default": TaskConfig(
        display_name="General conversation"
    ),
    "Text Analysis": TaskConfig(
        display_name="Detailed analysis of text"
    ),
    "Flashcards": TaskConfig(
        display_name="Practice with flashcards",
        requires_vocabulary=True,
        instructions="Type 'start' to begin practicing with your saved vocabulary words using flashcards. I will show you words in your target language, and you'll need to provide the translation."
    ),
    "Random Words": TaskConfig(
        display_name="Practice with random words",
        instructions="Type 'start' to begin practicing with randomly generated words. I will provide words in your target language, and you'll need to translate them."
    ),
    "Fill in the Blank": TaskConfig(
        display_name="Complete sentences by filling in missing words",
        instructions="Type 'start' to begin the fill-in-the-blank exercise. I will show you sentences with missing words, and you'll need to guess the correct word that fits in the blank."
    )
}

# Default values for settings
DEFAULT_INTERFACE_LANGUAGE = "English"
DEFAULT_LEARNING_LANGUAGE = "English"
DEFAULT_CURRENT_TASK = "Default"
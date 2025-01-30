from dataclasses import dataclass
from typing import Dict

@dataclass
class TaskConfig:
    display_name: str
    requires_vocabulary: bool = False

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
        requires_vocabulary=True
    ),
    "Random Words": TaskConfig(
        display_name="Practice with random words"
    ),
    "Fill in the Blank": TaskConfig(
        display_name="Practice by filling in missing words"
    )
}

# Default values for settings
DEFAULT_INTERFACE_LANGUAGE = "English"
DEFAULT_LEARNING_LANGUAGE = "English"
DEFAULT_CURRENT_TASK = "Default"
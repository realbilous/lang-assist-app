from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.prompts.text_analysis import TEXT_ANALYSIS_PROMPT
from src.prompts.general_prompts import DEFAULT_SYSTEM_PROMPT
from src.prompts.vocabulary_prompts import VOCABULARY_AUTOFILL_PROMPT
from src.prompts.exercise_prompts import (
    FLASHCARDS_PROMPT, 
    RANDOM_WORDS_PROMPT, 
    FILL_IN_BLANK_PROMPT
)

PROMPT_TEMPLATES = {
    "Default": ChatPromptTemplate.from_messages([
        ("system", DEFAULT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]),
    "Text Analysis": ChatPromptTemplate.from_messages([
        ("system", TEXT_ANALYSIS_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]),
    "Vocabulary Autofill": ChatPromptTemplate.from_messages([
        ("system", VOCABULARY_AUTOFILL_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]),
    "Flashcards": ChatPromptTemplate.from_messages([
        ("system", FLASHCARDS_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]),
    "Random Words": ChatPromptTemplate.from_messages([
        ("system", RANDOM_WORDS_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]),
    "Fill in the Blank": ChatPromptTemplate.from_messages([
        ("system", FILL_IN_BLANK_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ])
}
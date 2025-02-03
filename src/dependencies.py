import logging
from typing import Optional
from functools import lru_cache
from src.database.vocabulary_repository import VocabularyRepository
from src.database.sqlite_repository import SQLiteVocabularyRepository
from src.OpenAIChatAPI import OpenAIChatAPI
from config.config import (
    DEFAULT_INTERFACE_LANGUAGE,
    DEFAULT_LEARNING_LANGUAGE,
    DEFAULT_CURRENT_TASK
)

class Dependencies:
    _vocab_repo: Optional[VocabularyRepository] = None
    _chat_api: Optional[OpenAIChatAPI] = None
    _logger = logging.getLogger(__name__)
    
    # Default configurations
    _default_interface_language = DEFAULT_INTERFACE_LANGUAGE
    _default_learning_language = DEFAULT_LEARNING_LANGUAGE
    _default_task = DEFAULT_CURRENT_TASK
    _default_user_id = "user123"

    @classmethod
    @lru_cache()
    def get_vocabulary_repository(cls) -> VocabularyRepository:
        if cls._vocab_repo is None:
            try:
                cls._vocab_repo = SQLiteVocabularyRepository()
            except Exception as e:
                cls._logger.error(f"Failed to initialize vocabulary repository: {str(e)}")
                raise
        return cls._vocab_repo

    @classmethod
    @lru_cache()
    def get_chat_api(cls) -> OpenAIChatAPI:
        if cls._chat_api is None:
            try:
                cls._chat_api = OpenAIChatAPI()
            except Exception as e:
                cls._logger.error(f"Failed to initialize chat API: {str(e)}")
                raise
        return cls._chat_api

    @classmethod
    def get_default_interface_language(cls) -> str:
        return cls._default_interface_language

    @classmethod
    def get_default_learning_language(cls) -> str:
        return cls._default_learning_language

    @classmethod
    def get_default_task(cls) -> str:
        return cls._default_task

    @classmethod
    def get_default_user_id(cls) -> str:
        return cls._default_user_id 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import empty_checkpoint
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import trim_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langchain_core.messages import BaseMessage, RemoveMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from typing import Sequence, Optional, List

from src.models.vocabulary_models import VocabularyEntryOutputModel
from src.prompts.prompt_templates import PROMPT_TEMPLATES

from config.secrets import OPENAI_API_KEY

import logging

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    learning_language: str
    interface_language: str
    task: str
    vocabulary: Optional[List[VocabularyEntryOutputModel]]

class OpenAIChatAPI:    
    """
    A Python class to interact with the OpenAI API 
    """

    def __init__(self,
                 model="gpt-4o-mini", 
                 temperature=0.7):    
        """
        Initializes the OpenAIChatAPI instance.

        Args:
            model (str): The OpenAI model to use (e.g., "gpt-4", "gpt-3.5-turbo")
            temperature (float): Controls the randomness of responses (0.0 to 1.0)
        """
        self.logger = logging.getLogger(__name__)
        
        try:
            self.workflow = StateGraph(state_schema=State)
            self.chat_model = ChatOpenAI(
                model=model, 
                temperature=temperature,
                api_key=OPENAI_API_KEY
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize chat model: {str(e)}")
            raise
        
        self.prompt_templates = PROMPT_TEMPLATES
        
        self.trimmer = trim_messages(
            max_tokens=1000,
            strategy="last",
            token_counter=self.chat_model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )
        
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self._call_model)

        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)
        
        self.conversations: dict[str, list[BaseMessage]] = {}

    def _call_model(self, state: State) -> dict[str, list[BaseMessage]]:
        trimmed_messages = self.trimmer.invoke(state["messages"])
        prompt_template = self.prompt_templates.get(state.get("task", "Default"))
        
        # Prepare prompt variables
        prompt_vars = {
            "messages": trimmed_messages,
            "learning_language": state["learning_language"],
            "interface_language": state["interface_language"]
        }
        
        # Add formatted vocabulary if available
        if "vocabulary" in state:
            formatted_vocab = "\n".join(
                entry.format_for_prompt() 
                for entry in state["vocabulary"]
            )
            prompt_vars["formatted_vocabulary"] = formatted_vocab
        
        prompt = prompt_template.invoke(prompt_vars)
        response = self.chat_model.invoke(prompt)
        return {"messages": [response]}

    def chat(self, 
             query: str, 
             user_id: str, 
             learning_language: str = "English",
             interface_language: str = "English",
             task: str = "Default",
             vocabulary: Optional[List[VocabularyEntryOutputModel]] = None) -> BaseMessage:
        """
        Send a message to the chat model and get a response.

        Args:
            query (str): The user's input message
            user_id (str): Unique identifier for the user
            learning_language (str): Language to learn (defaults to English)
            interface_language (str): Interface language (defaults to English)
            task (str): Type of task (defaults to "Default")
            vocabulary (Optional[List[VocabularyEntryOutputModel]]): List of vocabulary entries for tasks that require it

        Returns:
            BaseMessage: The model's response
        """
        try:
            config = {"configurable": {"thread_id": user_id}}
            
            state_dict = {
                "messages": [HumanMessage(content=query)],
                "learning_language": learning_language,
                "interface_language": interface_language,
                "task": task
            }
            
            if vocabulary is not None:
                state_dict["vocabulary"] = vocabulary
            
            output = self.app.invoke(state_dict, config)
            
            return output["messages"][-1]
        except Exception as e:
            self.logger.error(f"Unexpected error during chat: {str(e)}")
            raise
    

    def delete_messages(self, user_id: str):
        config = {"configurable": {"thread_id": user_id}}

        messages = self.app.get_state(config).values.get("messages", [])
        
        if messages:          
            self.app.update_state(config, {"messages": [RemoveMessage(id=message.id) for message in messages]})

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import trim_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from typing import Sequence
from prompts.text_analysis import TEXT_ANALYSIS_PROMPT
from prompts.general_prompts import DEFAULT_SYSTEM_PROMPT

from config.secrets import OPENAI_API_KEY

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    learning_language: str
    interface_language: str
    task: str

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
        self.workflow = StateGraph(state_schema=State)
        self.chat_model = ChatOpenAI(model=model, 
                                     temperature=temperature,
                                     api_key=OPENAI_API_KEY)
        self.prompt_templates = {
            "Default": ChatPromptTemplate.from_messages([
                ("system", DEFAULT_SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="messages"),
            ]),
            "Text Analysis": ChatPromptTemplate.from_messages([
                ("system", TEXT_ANALYSIS_PROMPT),
                MessagesPlaceholder(variable_name="messages"),
            ])
        }

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
        prompt = prompt_template.invoke(
            {"messages": trimmed_messages, 
             "learning_language": state["learning_language"], 
             "interface_language": state["interface_language"]}
        )
        response = self.chat_model.invoke(prompt)
        return {"messages": [response]}

    def chat(self, 
             query: str, 
             user_id: str, 
             learning_language: str = "English",
             interface_language: str = "English",
             task: str = "Default") -> BaseMessage:
        """
        Send a message to the chat model and get a response.

        Args:
            query (str): The user's input message
            user_id (str): Unique identifier for the user
            language (str): Language for the response (defaults to English)

        Returns:
            BaseMessage: The model's response
        """
        config = {"configurable": {"thread_id": user_id}}
        
        output = self.app.invoke(
            {
                "messages": [HumanMessage(content=query)],
                "learning_language": learning_language,
                "interface_language": interface_language,
                "task": task
            },
            config,
        )
        
        return output["messages"][-1]
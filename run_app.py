import streamlit as st
from src.OpenAIChatAPI import OpenAIChatAPI
from config.config import (
    INTERFACE_LANGUAGES, 
    LEARNING_LANGUAGES, 
    TASK_OPTIONS,
    DEFAULT_INTERFACE_LANGUAGE,
    DEFAULT_LEARNING_LANGUAGE,
    DEFAULT_CURRENT_TASK
)

def main():
    st.set_page_config(page_title="Language Learning Assistant", layout="wide")
    
    # Initialize session state variables with defaults
    if 'chat_api' not in st.session_state:
        st.session_state.chat_api = OpenAIChatAPI()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'interface_language' not in st.session_state:
        st.session_state.interface_language = DEFAULT_INTERFACE_LANGUAGE
    if 'learning_language' not in st.session_state:
        st.session_state.learning_language = DEFAULT_LEARNING_LANGUAGE
    if 'current_task' not in st.session_state:
        st.session_state.current_task = DEFAULT_CURRENT_TASK

    # Sidebar for settings
    with st.sidebar:
        st.title("Settings")
        
        # Language Settings first
        st.title("Language Settings")
        st.session_state.interface_language = st.selectbox(
            "Your language:",
            options=INTERFACE_LANGUAGES,
            index=INTERFACE_LANGUAGES.index(st.session_state.interface_language)
        )
        st.session_state.learning_language = st.selectbox(
            "Language to learn:",
            options=LEARNING_LANGUAGES,
            index=LEARNING_LANGUAGES.index(st.session_state.learning_language)
        )
        
        st.divider()
        
        # Task selector below language settings
        st.title("Task Settings")
        st.session_state.current_task = st.selectbox(
            "Select task:",
            options=list(TASK_OPTIONS.keys()),
            format_func=lambda x: f"{TASK_OPTIONS[x]}",
            index=list(TASK_OPTIONS.keys()).index(st.session_state.current_task)
        )
        
        st.divider()
        
        # Clear chat button at the bottom
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    st.title("Language Learning Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about language learning..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_api.chat(
                    prompt,
                    "user123",
                    learning_language=st.session_state.learning_language,
                    interface_language=st.session_state.interface_language,
                    task=st.session_state.current_task
                ).content
                st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
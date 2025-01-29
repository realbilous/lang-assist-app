import streamlit as st
import pandas as pd

from src.OpenAIChatAPI import OpenAIChatAPI
from config.config import (
    INTERFACE_LANGUAGES, 
    LEARNING_LANGUAGES, 
    TASK_OPTIONS,
    DEFAULT_INTERFACE_LANGUAGE,
    DEFAULT_LEARNING_LANGUAGE,
    DEFAULT_CURRENT_TASK
)
from src.database.models import VocabularyEntry
from src.database.sqlite_repository import SQLiteVocabularyRepository

def create_vocabulary_table():
    entries = st.session_state.vocab_repo.get_entries("user123")
    if entries:
        table_data = []
        # Create table data without direct checkbox widgets
        for _, entry in enumerate(entries):
            definitions_text = "\n".join(entry.definitions) if entry.definitions else ""
            is_selected = entry.word_phrase in st.session_state.selected_words
            table_data.append({
                "Select": is_selected,
                "Word/Phrase": entry.word_phrase,
                "Translation": entry.translation,
                "Definitions": definitions_text,
                "Example": entry.example_sentence
            })
        
        df = pd.DataFrame(table_data)
        
        # Create the selection interface using st.data_editor instead of st.dataframe
        edited_df = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    default=False,
                )
            },
            key="data_editor"
        )
        
        # Update selected_words based on the edited dataframe
        st.session_state.selected_words = {
            row["Word/Phrase"] 
            for _, row in edited_df.iterrows() 
            if row.get("Select", False)
        }
    else:
        st.info("No vocabulary entries yet.")

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
    if 'selected_words' not in st.session_state:
        st.session_state.selected_words = set()

    # Sidebar for settings
    with st.sidebar:
        st.title("Controls")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Vocab", use_container_width=True):
                st.session_state.current_page = "vocabulary"
                st.rerun()
        with col2:
            if st.button("Chat", use_container_width=True):
                st.session_state.current_page = "chat"
                st.rerun()
        with col3:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

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
        
        # Task selector below language settings
        st.title("Task Settings")
        st.session_state.current_task = st.selectbox(
            "Select task:",
            options=list(TASK_OPTIONS.keys()),
            format_func=lambda x: f"{TASK_OPTIONS[x]}",
            index=list(TASK_OPTIONS.keys()).index(st.session_state.current_task)
        )


    # Main interface
    if getattr(st.session_state, 'current_page', 'chat') == 'vocabulary':
        st.title("My Vocabulary")
        
        # Initialize vocabulary repository if not exists
        if 'vocab_repo' not in st.session_state:
            st.session_state.vocab_repo = SQLiteVocabularyRepository()

        # Top panel with buttons
        button_col1, button_col2, button_col3 = st.columns([1, 1, 8])  # Adjust ratio for button spacing
        with button_col1:
            if st.button("Add Entry", use_container_width=True):
                st.session_state.show_add_entry_modal = not getattr(st.session_state, 'show_add_entry_modal', False)
                st.rerun()
        with button_col2:
            if len(st.session_state.selected_words) > 0:
                with st.popover("Delete"):
                    num_selected = len(st.session_state.selected_words)
                    st.write(f"Are you sure you want to delete {num_selected} selected word{'s' if num_selected > 1 else ''}?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes", use_container_width=True):
                            # TODO: Improve deletion performance, so that it's not necessary to iterate over all entries. Use unique record ids instead.
                            for word in st.session_state.selected_words:
                                # Find and delete each selected entry
                                entries = st.session_state.vocab_repo.get_entries("user123")
                                for entry in entries:
                                    if entry.word_phrase == word:
                                        st.session_state.vocab_repo.delete_entry(entry.entry_id)
                            st.session_state.selected_words = set()
                            st.rerun()
                    with col2:
                        if st.button("No", use_container_width=True):
                            st.rerun()
            else:
                st.button("Delete", use_container_width=True, disabled=True)

        # Main content area
        if getattr(st.session_state, 'show_add_entry_modal', False):
            # Split screen when form is shown
            table_col, form_col = st.columns(2)
            
            # Table in left column
            with table_col:
                create_vocabulary_table()
            
            # Form in right column
            with form_col:
                with st.form("add_vocabulary_modal"):
                    st.subheader("Add New Entry")
                    word_phrase = st.text_input("Word/Phrase")
                    translation = st.text_input("Translation")
                    definitions = st.text_area("Definitions (one per line)")
                    example = st.text_input("Example sentence")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Add")
                    with col2:
                        cancel = st.form_submit_button("Cancel")
                    
                    if submit and word_phrase and translation:
                        entry = VocabularyEntry(
                            entry_id=0,
                            user_id="user123",
                            learning_language=st.session_state.learning_language,
                            interface_language=st.session_state.interface_language,
                            word_phrase=word_phrase,
                            translation=translation,
                            definitions=definitions.split('\n') if definitions else [],
                            example_sentence=example
                        )
                        st.session_state.vocab_repo.add_entry(entry)
                        st.session_state.show_add_entry_modal = False
                        st.success("Word added successfully!")
                        st.rerun()
                    
                    if cancel:
                        st.session_state.show_add_entry_modal = False
                        st.rerun()
        else:
            create_vocabulary_table()

    else:
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
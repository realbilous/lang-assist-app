# lang-assist-app
LLM backed language assistant for language learning.
## Overview
Lang-assist-app is an AI-powered language learning assistant that provides interactive language learning features through Large Language Models (LLMs). The application offers various tools to help users learn and practice their target language effectively.

![Start view of the chat interface](./tutorial/start_view_chat.JPG)

## Features


### 1. Text Analysis
- Detailed sentence-by-sentence breakdown of texts
- Word and phrase level analysis including:
  - Translations
  - Multiple definitions
  - Usage examples
  - Grammar explanations
- Comprehensive grammar analysis for each sentence

### 2. Vocabulary Tools
- Vocabulary autofill with detailed word information
  ![Add entry to the vocabulary](./tutorial/view_vocab_add_entry.JPG)
  ![Autofill vocabulary entry](./tutorial/view_vocab_autofill.JPG)
- Flashcard generation for vocabulary practice
- Random word generation for vocabulary expansion
- Fill-in-the-blank exercises
  ![Fill-in-the-blank exercises](./tutorial/view_vocab_fillin_exercise.JPG) 


### 3. Interactive Learning
- Customizable interface language
- Support for multiple target languages
- Natural conversation capabilities with AI language teacher

## Setup

1. Clone the repository
2. Set up your environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
3. Install dependencies (requirements.txt file)
4. Run the application

## Usage

To start the application, run the following command in the repository root:

```streamlit run run_app.py```

When the app starts, you will be provided with a local URL to access it.

The application provides several prompt templates for different learning activities:

1. **General conversation**: General language learning assistance and conversations
2. **Detailed analysis of text**: Deep dive into text comprehension and grammar
3. **Practice with flashcards**: Practice your custom vocabulary and phrases
4. **Practice with random words**: Expand your vocabulary with random word exercises
5. **Complete sentences by filling in missing words**: Interactive exercises to practice vocabulary in context

Each mode is designed to help learners understand and practice their target language effectively while receiving feedback and explanations in their preferred interface language.

## Configuration

The application can be configured with:
- Learning language (target language you want to learn)
- Interface language (language for instructions and explanations)
- Tasks (described above)
- Switch between chat and vocabulary views
- Select the user id (each user has their own vocabulary and chat progress)
- (Advanced) Custom prompt templates for specialized learning activities

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or bug fixes.

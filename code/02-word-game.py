# 02-word-game.py
# Deck 01: Talking with LLMs via code (Anatomy of a conversation)
# Goal: play a word guessing game where the LLM is the guesser. The first user
# message includes a modifier (e.g. "In British English,") that steers later
# turns; this shows how the conversation carries state in the message history.

# %% Import packages and load environment variable for API access
import chatlas
import dotenv
dotenv.load_dotenv()

# %% Set up a chat with a system prompt
chat = chatlas.ChatAnthropic(
    system_prompt="We are playing a word guessing game. "
    "At each turn, you guess the word and tell us what it is."
)
chat.chat("In British English, guess the word for a person who lives next door.")
chat.chat("What helps a car move smoothly down the road?")

# %% Compare with...
chat2 = chatlas.ChatAnthropic()
chat2.chat("What helps a car move smoothly down the road?")

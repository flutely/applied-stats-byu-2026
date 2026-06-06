# 02-word-game.R
# Deck 01: Talking with LLMs via code (Anatomy of a conversation)
# Goal: play a word guessing game where the LLM is the guesser. The first user
# message includes a modifier (e.g. "In British English,") that steers later
# turns; this shows how the conversation carries state in the message history.

# %% Import package
library(ellmer)

# %% Set up a chat with a system prompt
chat <- chat_anthropic(
  system_prompt = paste(
    "We are playing a word guessing game.",
    "At each turn, you guess the word and tell us what it is."
  )
)

# Ask the first question:
chat$chat("In British English, guess the word for the person who lives next door.")

# Ask the second question:
chat$chat("What helps a car move smoothly down the road?")

# %% Compare with...
chat2 <- chat_anthropic()
chat2$chat("What helps a car move smoothly down the road?")

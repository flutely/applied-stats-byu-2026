# 11-quiz-game-app.py
# Deck 03: Prompt engineering and RAG (Prompt engineering and hallucinations)
# Goal: write the system prompt for the quiz game show. Iterate on it and test
# against a few user messages.

import chatlas
import dotenv
from pyhere import here
from shiny import App, reactive, ui

dotenv.load_dotenv()

# UI ---------------------------------------------------------------------------

app_ui = ui.page_fillable(
    ui.chat_ui("chat"),
)


def server(input, output, session):
    chat_ui = ui.Chat(id="chat")

    # Set up the chat instance
    client = chatlas.ChatAnthropic(
        model="claude-sonnet-4-6",
        system_prompt=here("code/11-quiz-game-prompt.md").read_text(encoding="utf-8"),
    )

    @chat_ui.on_user_submit
    async def handle_user_input(user_input: str):
        # Use `content="all"` to include tool calls in the response stream
        response = await client.stream_async(user_input, content="all")
        await chat_ui.append_message_stream(response)

    @reactive.effect
    def _():
        # Start the game when the app launches
        chat_ui.update_user_input(value="Let's play the quiz game!", submit=True)


app = App(app_ui, server)

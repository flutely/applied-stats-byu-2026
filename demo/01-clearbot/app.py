import json
import os
from pathlib import Path
from typing import Iterable, TypeAlias

import chatlas
from dotenv import load_dotenv
from offcanvas import offcanvas_ui
from pydantic import BaseModel
from shiny import App, Inputs, Outputs, Session, bookmark, reactive, render, req, ui
from starlette.requests import Request
from tools import all_tools

# chatlas 0.18's base Turn is not generic (only AssistantTurn is), and these lists
# hold every turn kind, so annotate with the plain base class.
MyTurn: TypeAlias = chatlas.Turn

load_dotenv()

model_options = {}

if "ANTHROPIC_API_KEY" in os.environ:
    model_options["Anthropic"] = {
        "claude-opus-4-8": "Claude Opus 4.8 (latest, smartest)",
        "claude-sonnet-4-6": "Claude Sonnet 4.6 (balanced)",
        "claude-haiku-4-5": "Claude Haiku 4.5 (fastest, cheapest)",
    }

if len(model_options) == 0:
    raise ValueError(
        "No API keys found. Please set ANTHROPIC_API_KEY in your environment."
    )


def app_ui(request: Request):
    return ui.page_sidebar(
        ui.sidebar(
            ui.input_select(
                "model",
                "Model",
                model_options,
                selected="claude-sonnet-4-6",
            ),
            ui.input_text_area("system_prompt", "System prompt", rows=6),
            ui.help_text("Instructs the LLM how to behave"),
            ui.input_checkbox_group(
                "tools",
                "Tools",
                {
                    "weather": "Weather",
                    "filesystem": "Filesystem access",
                    "websearch": "Web search",
                },
            ),
            width=325,
            title="Settings",
            open="closed",
        ),
        ui.tags.script(src="new-chat-button.js"),
        offcanvas_ui(
            "trace",
            "Trace Inspector",
            ui.TagList(
                ui.input_select("trace_num", "Select a trace", []),
                ui.output_ui("trace_display"),
            ),
            style="--bs-offcanvas-width: min(600px, 100vw);",
        ),
        ui.chat_ui("chat"),
        ui.head_content(
            ui.tags.script(src="json-viewer.js"),
            ui.tags.script(src="main.js"),
            ui.tags.style(
                """
                .help-block {
                    margin-top: -1em;
                }
                """
            ),
        ),
        title="Clearbot",
        fillable=True,
    )


class RequestParams(BaseModel):
    """A snapshot of the parameter values at the moment of a request"""

    model: str
    user_prompt: str
    system_prompt: str
    tools: list[str]


class SessionState(BaseModel):
    turns: list[MyTurn]
    snapshots: list[tuple[RequestParams, list[MyTurn]]]


def server(input: Inputs, output: Outputs, session: Session):
    turns: reactive.Value[list[MyTurn]] = reactive.Value([])
    snapshots: reactive.Value[list[tuple[RequestParams, list[MyTurn]]]] = (
        reactive.Value([])
    )

    chat = ui.Chat("chat")

    def current_params(user_prompt: str) -> RequestParams:
        return RequestParams(
            model=input.model(),
            user_prompt=user_prompt,
            system_prompt=input.system_prompt(),
            tools=input.tools(),
        )

    @chat.on_user_submit
    async def chat_on_user_submit(user_prompt: str):
        these_turns = turns()
        params: RequestParams = current_params(user_prompt)

        chat_client = chatlas.ChatAnthropic(
            model=params.model,
            system_prompt=params.system_prompt,
        )

        chat_client.set_turns(these_turns)

        for toolset in input.tools():
            for tool in all_tools[toolset]:
                chat_client.register_tool(tool)

        resp = await chat_client.stream_async(params.user_prompt)

        async def gen():
            async for chunk in resp:
                yield chunk
            with reactive.isolate():
                yield button_for_index(len(snapshots.get()))

        task = await chat.append_message_stream(gen())

        @reactive.Effect
        async def resp_on_complete():
            if task.status() == "success":
                resp_on_complete.destroy()
                turns.set(chat_client.get_turns())
                turns_snapshot = chat_client.get_turns(include_system_prompt=True)
                snapshots.set(snapshots.get() + [(params, turns_snapshot)])
                with reactive.isolate():
                    ui.update_select(
                        "trace_num", choices=list(range(len(snapshots.get())))
                    )
                await session.bookmark()
            if task.status() in ["error", "cancelled"]:
                resp_on_complete.destroy()

    @session.bookmark.on_bookmarked
    async def session_on_bookmarked(url: str):
        print("session_on_bookmarked")
        await session.bookmark.update_query_string(mode="replace")

    @session.bookmark.on_bookmark
    def session_on_bookmark(state: bookmark.BookmarkState):
        ss = SessionState(turns=turns(), snapshots=snapshots())
        print(ss.model_dump_json())
        state.values["session_state"] = ss.model_dump(mode="json")

    @session.bookmark.on_restore
    async def session_on_restore(state: bookmark.BookmarkState):
        if "session_state" in state.values:
            ss = SessionState.model_validate(state.values["session_state"])
            last_turns = ss.snapshots[-1][1]
            turns.set(last_turns)
            snapshots.set(ss.snapshots)
            ui.update_select("trace_num", choices=list(range(len(snapshots.get()))))

            i = 0
            for turn in last_turns:
                if turn.role == "assistant":
                    suffix = button_for_index(i)
                    i += 1
                else:
                    suffix = ""
                await chat.append_message(
                    {
                        "role": turn.role,
                        "content": "\n".join([str(x) for x in turn.contents]) + suffix,
                    }
                )

    @reactive.effect
    @reactive.event(input.clear)
    async def clear_messages():
        print("Clearing messages")
        await chat.clear_messages()
        turns.set([])
        snapshots.set([])

    def button_for_index(i: int) -> str:
        return f"""\n\n<a class="text-decoration-none" href="#" data-snapshot-index="{i}" title="Inspect this request/response">{{…}}</a>"""

    @render.ui
    def trace_display():
        req(len(snapshots()) > 0)
        (params, turns) = snapshots()[
            int(input.trace_num()) or 0
            if "trace_num" in input and input.trace_num() is not None
            else 0
        ]

        dump = reconstruct_request_traces(params, turns[0:-1])
        print(json.dumps(dump, indent=2))

        resp = reconstruct_response_traces(turns[-1])

        return ui.TagList(
            ui.h4("Request"),
            # ui.Tag("json-viewer", data=params.model_dump_json(indent=2)),
            ui.Tag("json-viewer", data=json.dumps(dump)),
            ui.h4("Response", class_="mt-3"),
            ui.Tag("json-viewer", data=json.dumps(resp)),
        )


def reconstruct_request_traces(
    params: RequestParams, turns: Iterable[MyTurn]
) -> dict[str, object]:
    """Reconstruct the Anthropic Messages API request from the conversation so far."""
    tools_schema = reconstruct_tools_schema(params.tools)

    system_prompt = None
    messages = []
    for turn in turns:
        data = json.loads(turn.model_dump_json())
        contents = data.get("contents") or []
        text = contents[0].get("text", "") if contents else ""
        if data["role"] == "system":
            if text:
                system_prompt = text
            continue
        messages.append({"role": data["role"], "content": text})

    request: dict[str, object] = {"model": params.model}
    if system_prompt:
        request["system"] = system_prompt
    if tools_schema:
        request["tools"] = tools_schema
    request["messages"] = messages
    return request


def reconstruct_tools_schema(toolsets: list[str]) -> list[object]:
    """Render each registered tool in Anthropic's {name, description, input_schema} form."""
    result = []
    for toolset in toolsets:
        for tool in all_tools[toolset]:
            # chatlas builds tool schemas in OpenAI function-call format; map to Anthropic's.
            schema = chatlas._tools.func_to_schema(tool)["function"]
            result.append(
                {
                    "name": schema["name"],
                    "description": schema.get("description", ""),
                    "input_schema": schema["parameters"],
                }
            )
    return result


def reconstruct_response_traces(turn: MyTurn) -> object:
    # AssistantTurn.completion holds the raw anthropic.types.Message returned by the
    # provider. Show it verbatim when available (live turns). It is excluded from
    # serialization, so for turns restored from a bookmark fall back to the contents.
    completion = getattr(turn, "completion", None)
    if completion is not None and hasattr(completion, "model_dump"):
        return completion.model_dump(mode="json")

    return {
        "role": turn.role,
        "content": [str(content) for content in turn.contents],
        "stop_reason": getattr(turn, "finish_reason", None),
    }


app = App(
    app_ui, server, bookmark_store="url", static_assets=Path(__file__).parent / "www"
)

from fasthtml.common import *
from app.agents.main_graph import main_graph

from langchain_core.messages import SystemMessage, AIMessage

from app.views.components.header import header_component
from app.views.components.message_bubble import message_bubble_component


def interview_view(request, id: str):

    state = main_graph.get_state(config={"configurable": {"thread_id": id}})
    messages = state.values.get("messages", [])
    messages = [
        ("AI", m.content) if isinstance(m, AIMessage) else ("ME", m.content)
        for m in messages
        if not isinstance(m, SystemMessage)
    ]

    question = state.values.get("interview_question", "")

    box_style = "border-radius: 3px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); background-color: var(--pico-card-background-color); height: 100%"
    return (
        Title("AI Coding Interview Agent"),
        header_component(),
        Main(
            cls="container",
            style="height: calc(100vh - 100px); max-width: 100%; width: 95%;",
        )(  # Adjust the 60px if needed
            Div(
                cls="interview-grid",
                style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; height: 100%;",
            )(
                Div(
                    style=box_style
                    + "height: 100%; display: flex; flex-direction: column;",
                    cls="chat-container",
                )(
                    H3("Chat", style="flex: 0 0 auto; margin-bottom: 10px;"),
                    Div(style="flex: 1; overflow-y: auto; margin-bottom: 10px;")(
                        *[
                            message_bubble_component(role=m[0], content=m[1])
                            for m in messages
                        ]
                    ),
                    Form(
                        hx_post="/chat",
                        hx_target=".chat-container",
                        hx_swap="beforeend",
                        style="flex: 0 0 auto; display: flex; gap: 10px;",
                    )(
                        Input(style="margin-bottom: 0; flex: 1;")(type="text"),
                        Button("Send"),
                    ),
                ),
                Div(
                    style="display: flex; flex-direction: column; gap: 10px; height: 100%"
                )(
                    Div(style=box_style)(H3("Code Editor")),
                    Div(style=box_style)(H3("Output")),
                ),
                Div(
                    style="display: flex; flex-direction: column; gap: 10px; height: 100%"
                )(
                    Div(style=box_style)(H3("Question"), P(question)),
                    Div(style=box_style)(H3("Test result"), P("Test result")),
                    Div(style="display: flex; gap: 10px; width: 100%;")(
                        Button(cls="primary", style="flex: 1; width: calc(50% - 5px);")(
                            "Get feedback"
                        ),
                        Button(
                            cls="contrast", style="flex: 1; width: calc(50% - 5px);"
                        )("Submit"),
                    ),
                ),
            ),
        ),
        Style(
            """
            @media (max-width: 1024px) {
                .interview-grid {
                    grid-template-columns: 1fr !important;
                    height: auto !important;
                }
                .chat-container {
                    height: 50vh !important;
                }
            }
        """
        ),
    )

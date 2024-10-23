from fasthtml.common import *


def message_bubble_component(role: str, content: str):
    return (
        Div(
            cls="message-bubble" + (" ai-message" if role == "AI" else " user-message"),
            style="display: flex; flex-direction: column; gap: 10px;",
        )(
            Div(cls="message-role")(role),
            Div(cls="message-content")(content),
        ),
        Style(
            """
    .message-bubble {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }
    .ai-message {
        background-color: var(--pico-mark-background-color);
    }
    .user-message {
        background-color: var(--pico-text-selection-color);
    }
    .message-role {
        font-weight: bold;
    }
    .message-content {
        flex: 1;
    }
    """
        ),
    )

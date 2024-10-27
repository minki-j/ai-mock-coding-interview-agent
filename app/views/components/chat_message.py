from fasthtml.common import *

def chat_message(role, content):
    alignment = "flex-start" if role == "AI" else "flex-end"

    return Div(
        Div(
            Div(  # Shows the Role
                Strong(role),
                style=f"font-size: 0.9em; letter-spacing: 0.05em;",
            ),
            Div(  # Shows content and applies font color to stuff other than syntax highlighting
                Style(
                    f".marked *:not(code):not([class^='hljs'])"
                ),
                P(content),
                style=f"margin-top: 0.5em;",
            ),
            # extra styling to make things look better
            style=f"""
                margin-bottom: 1em; padding: 1em; border: 0.5px solid var(--pico-border-color); border-radius: 24px;
                max-width: 70%; position: relative; box-shadow: 0 0 10px rgba(0,0,0,0.1);""",
        ),
        style=f"display: flex; justify-content: {alignment};",
    )

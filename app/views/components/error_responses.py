from fasthtml.common import *


def error_modal(message: str, status_code: int = 500):
    return Response(
        to_xml(
            Div(
                cls="error-modal",
            )(
                Div(
                    cls="error-content",
                )(
                    Button(
                        "×",
                        cls="btn-loader close-btn",
                        onclick="this.parentElement.parentElement.remove()",
                    ),
                    H2("Error"),
                    P(message),
                ),
            ),
        ),
        status_code=status_code,
        headers={"HX-Replace-Url": "false"},  # Prevent the URL from being replaced
    )

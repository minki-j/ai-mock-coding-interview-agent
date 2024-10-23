from fasthtml.common import *


def header_component():
    return (
        Header(
            cls="container",
            style="display: flex; justify-content: space-between; align-items: center; max-width: 100%; width: 95%;",
        )(
            A(href="/", style="text-decoration: none;")(
                H1(
                    "AI Coding Interview Agent",
                    style="font-weight: 900; font-size: 2.8rem; color: #4A4A4A; margin: 0; text-transform: uppercase; letter-spacing: 1px;",
                )
            ),
            Div(cls="profile-section")(
                Details(cls="dropdown", style="margin: 0;")(
                    Summary("Profile"),
                    Ul(
                        Li(A(href="/profile")("View Profile")),
                        Li(A(href="/settings")("Settings")),
                        Li(A(href="/logout")("Logout")),
                    ),
                )
            ),
        ),
    )

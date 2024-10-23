from fasthtml.common import *
from fasthtml.oauth import GoogleAppClient
from urllib.parse import urljoin

from app.views.components.header import header_component

client = GoogleAppClient(
    os.getenv("AUTH_CLIENT_ID"),
    os.getenv("AUTH_CLIENT_SECRET"),
)
auth_callback_path = "/auth_redirect"

def login_view(request):
    print("\n>>> VIEW: login_view")
    protocol = request.headers.get("X-Forwarded-Proto", "http")
    base_url = f"{protocol}://{request.headers['host']}"
    redir = urljoin(base_url, auth_callback_path)
    print(f"==>> redir: {redir}")
    login_link = client.login_link(redir)

    return (
        Title("AI Coding Interview Agent"),
        Main(cls="container")(
            P("Please login to continue."),
            A(
                Button(
                    Img(
                        src="/static/google_logo.png",
                        alt="Google logo",
                        style="width: 18px; height: 18px; margin-right: 8px;",
                    ),
                    "Sign in with Google",
                    style="display: flex; align-items: center; justify-content: center;",
                ),
                href=login_link,
                style="display: inline-block; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-family: Arial, sans-serif; ",
            ),
        ),
    )

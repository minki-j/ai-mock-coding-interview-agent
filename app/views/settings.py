from fasthtml.common import *

def settings_view(request):
    return (
        Title("Settings"),
        Main(cls="container")(
            P("Settings"),
        ),
    )

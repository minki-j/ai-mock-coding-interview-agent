from fasthtml.common import *

def profile_view(request):
    return (
        Title("Profile"),
        Main(cls="container")(
            P("Profile"),
        ),
    )

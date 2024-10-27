from fasthtml.common import *

from app.agents.main_graph import main_graph
from app.views.components.chat_message import chat_message

async def chat(request, id: str):
    form_data = await request.form()
    message = form_data.get("message")

    config = {"configurable": {"thread_id": id}}
    main_graph.update_state(
        config,
        {"messages": [{"role": "user", "content": message}]}
    )
    response = main_graph.invoke(None, config)

    return chat_message("user", message), chat_message("AI", response["message_from_interviewer"])

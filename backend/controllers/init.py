import json
import uuid
from datetime import datetime

from fasthtml.common import *
from views.components.error_responses import error_modal

from agents.main_graph import main_graph

from db import db


async def initialize_interview(session, request: Request):
    print("\n>>> CNTRL initialize_interview")

    interview_id = str(uuid.uuid4())

    form_data = await request.form()

    response = main_graph.invoke(
        input={
            "difficulty_level": form_data["difficulty"],
            "interview_question": form_data["question"],
            "interview_solution": form_data["solution"],
        },
        config={"configurable": {"thread_id": interview_id}, "recursion_limit": 100},
    )

    if response:
        db.t.interviews.insert(
            id=interview_id,
            user_id=session["user_id"],
            created_at=datetime.now().isoformat(),
        )
        print(f"\n>>> Interview inserted with id: {interview_id}")

        return RedirectResponse(url=f"/interview?id={interview_id}", status_code=303)
    else:
        return error_modal("An error happened at generate_interview")

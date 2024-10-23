import json
from fasthtml.common import *
from db import db


async def update_profile(req, session):
    print("\n>>> CNTRL: update_profile")
    form_data = await req.form()
    
    user_id = session["user_id"]
    user_data = db.t.users.get(user_id)

    db.t.users.update(
        pk_values=user_id,
        updates={
            
        },
    )

    return Response("", 204)

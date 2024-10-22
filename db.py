import os
import json
from fasthtml.common import *
from langchain_core.messages import AnyMessage

os.makedirs("./data/main_database", exist_ok=True)
db_path = os.path.join(".", "data", "main_database", "main.db")

print(f">>>> DB: initialize database at {db_path}")
db = database(db_path)

users, interviews = (db.t.users, db.t.interviews)

if users not in db.t:
    print("\n>>>> DB: Creating users table")
    users.create(
        id=str,
        name=str,
        email=str,
        pk="id",
    )

if interviews not in db.t:
    print("\n>>>> DB: Creating interviews table")
    interviews.create(
        id=str,
        user_id=str,
        created_at=str,
        pk="id",
        foreign_keys=(("user_id", "users")),
        if_not_exists=True,
        # Messages will be stored in the LangGraph State
    )

Users = users.dataclass()
Interviews = interviews.dataclass()

# try:
#     main_db_diagram = diagram(db.tables)
#     main_db_diagram.render(
#         "data/main_database/main_db_diagram", format="png", cleanup=True
#     )
# except:
#     print(
#         "Error on generating DB visualization. Probably graphviz executables were not found. Please install Graphviz and add it to your system's PATH."
#     )

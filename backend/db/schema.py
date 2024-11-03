from typing import Annotated
import datetime
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

class Interview(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    interview_question: str
    interview_solution: str
    user_id: int = Field(foreign_key="user.id")

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message: str
    sent_time: datetime.datetime = Field(default=datetime.datetime.now())
    sender: Literal["AI", "USER"]
    interview_id: int = Field(foreign_key="interview.id")

class CodeEditorState(SQLModel, table=True):
    # Only update when the code is ran
    id: int | None = Field(default=None, primary_key=True)
    code: str
    test_result: str
    interview_id: int = Field(foreign_key="interview.id")

    
import datetime
from typing import Literal, Optional
from pydantic import BaseModel

class Interview(BaseModel):
    id: Optional[str] = None
    interview_question: str
    interview_solution: str
    user_id: str

class Message(BaseModel):
    id: Optional[str] = None
    message: str
    sent_time: datetime.datetime = datetime.datetime.now()
    sender: Literal["AI", "USER"]
    interview_id: str

class CodeEditorState(BaseModel):
    id: Optional[str] = None
    code: str
    test_result: str
    interview_id: str

    
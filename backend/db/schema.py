import datetime
from typing import Literal, Optional
from pydantic import BaseModel

class Interview(BaseModel):
    id: Optional[str] = None
    interview_question: str
    interview_solution: str
    user_id: str
    final_solution: str
    test_result: str
    feedback: str
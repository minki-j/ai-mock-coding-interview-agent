import datetime
import uuid
import operator
from typing import Annotated, TypedDict, Dict, List
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

from app.agents.subgraphs.thought_process.prompts import default_system_message

INTERVIEW_TIME_IN_SECONDS = 60 # 45 minutes
THOUGHT_TIME_IN_SECONDS = 20 # 10 minutes

# ===========================================
#                VARIABLE SCHEMA
# ===========================================


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================


# ===========================================
#                    STATE
# ===========================================
class InputState(BaseModel):
    difficulty_level: Literal["easy", "medium", "hard"] = Field(default="easy")
    interview_question: str = Field(default="")
    interview_solution: str = Field(default="")
    user_solution: str = Field(default="")

class OutputState(BaseModel):
    message_from_interviewer: str = Field(default="")

class OverallState(InputState, OutputState):
    start_time: datetime.datetime = None

    def is_thought_process_stage(self):
        if not self.start_time:
            return True
        return (datetime.datetime.now() - self.start_time).total_seconds() <= THOUGHT_TIME_IN_SECONDS

    code_editor_state: str = Field(default="TESTCODEEDITORSTATE")

    messages: Annotated[list[AnyMessage], add_messages] = Field(default_factory=lambda: [default_system_message]) #! Default messages is not working

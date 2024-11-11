import datetime
import uuid
import operator
from typing import Annotated, TypedDict, Dict, List
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

from agents.subgraphs.thought_process.prompts import default_system_message

INTERVIEW_TIME_IN_MINUTES = 60  # 45 minutes
THOUGHT_TIME_IN_MINUTES = 10  # 10 minutes

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
    interviewee_name: str = Field(default="")
    difficulty_level: Literal["easy", "medium", "hard"] = Field(default="easy")
    interview_question: str = Field(default="")
    interview_solution: str = Field(default="")


class OutputState(BaseModel):
    message_from_interviewer: str = Field(default="")


class OverallState(InputState, OutputState):
    greeting_msg_index: int = Field(default=0)
    stage: Literal["greeting", "thought_process", "coding", "assessment"] = Field(
        default="greeting"
    )
    thought_process_summary: str = Field(default="")

    # TODO: evolution of the code and test result.
    code_editor_state: str = Field(default="")
    test_result: str = Field(default="")

    messages: Annotated[list[AnyMessage], add_messages] = Field(
        default_factory=lambda: [default_system_message]
    )  #! Default messages is not working

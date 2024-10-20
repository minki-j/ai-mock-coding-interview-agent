import uuid
import operator
from typing import Annotated, TypedDict, Dict, List
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

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

class OutputState(BaseModel):
    interview_question: str = Field(default="")
    message_from_interviewer: str = Field(default="")

class OverallState(InputState, OutputState):
    is_thought_process_stage: bool = False
    is_question_generated: bool = False


    code_editor_state: str = Field(default="")

    messages: Annotated[list[AnyMessage], add_messages]

import datetime
import uuid
import operator
from typing import Annotated, TypedDict, Dict, List
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

from agents.subgraphs.thought_process_stage.prompts import default_system_message


# ===========================================
#                VARIABLE SCHEMA
# ===========================================


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================
def replace_with_new_state(_, new):
    return new


# ===========================================
#                    STATE
# ===========================================
class InputState(BaseModel):
    start_date: str = Field(default="")
    interviewee_name: str = Field(default="")
    difficulty_level: Literal["easy", "medium", "hard"] = Field(default="easy")
    interview_title: str = Field(default="")
    interview_question: str = Field(default="")
    interview_question_md: str = Field(default="")
    interview_approaches: list[dict] = Field(default=[])
    test_code: str = Field(default="")
    code_snippet: list[dict] = Field(default=[])
    test_input_output: list[dict] = Field(default=[])


class OutputState(BaseModel):
    message_from_interviewer: Annotated[str, replace_with_new_state] = Field(default="")
    stage: Literal["greeting", "thought_process", "main", "assessment"] = Field(
        default="greeting"
    )
    main_stage_step: Literal["coding", "debugging", "algorithmic_analysis"] = Field(
        default="coding"
    )
    display_decision: str = Field(default="")


class OverallState(InputState, OutputState):
    greeting_msg_index: int = Field(default=0)
    thought_process_summary: str = Field(default="")

    # TODO: evolution of the code and test result.
    code_editor_state: str = Field(default="")
    user_approach: str = Field(default="")
    test_result: str = Field(default="")

    messages: Annotated[list[AnyMessage], add_messages] = Field(
        default_factory=lambda: [default_system_message]
    )  #! Default messages is not working

    def stringify_messages(self):
        stringified_messages = "\n\n".join(
            [
                f">>{message.type.upper()}: {message.content}"
                for message in self.messages[1:]
            ]
        )
        return stringified_messages

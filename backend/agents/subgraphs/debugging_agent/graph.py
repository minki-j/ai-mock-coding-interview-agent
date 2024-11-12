import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm_models import chat_model


class CodeFeedbackAgentPrivateState(BaseModel):
    interview_question: str = Field(default="")
    interview_solution: str = Field(default="")
    code_editor_state: str = Field(default="")

    debugging_result: str = Field(default="")
    assessment_result: str = Field(default="")

class DebuggingAgentPrivateState(BaseModel):
    interview_question: str = Field(default="")
    interview_solution: str = Field(default="")
    code_editor_state: str = Field(default="")

    debugging_record: list[str] = Field(default=[])


def initiate_private_state(state):
    print("initiate_private_state: \n", state.__annotations__)
    print("type: ", type(state))
    return {
        "interview_question": state.interview_question,
        "interview_solution": state.interview_solution,
        "code_editor_state": state.code_editor_state,
    }


def placeholder_node(state: DebuggingAgentPrivateState):
    return {
        "debugging_record": ["debugging_record testing"],
    }


def placeholder_node2(state: DebuggingAgentPrivateState):
    return {
        "debugging_result": "debugging_result testing",
    }

def last_node(state: CodeFeedbackAgentPrivateState):

    print("last_node CodeFeedbackAgentPrivateState debugging_result: \n", state.debugging_result)
    return {
        "debugging_result": state.debugging_result, #? BUG: this return is applied to OverallState instead of CodeFeedbackAgentPrivateState
    }

g = StateGraph(CodeFeedbackAgentPrivateState)
g.add_edge(START, n(initiate_private_state))

g.add_node(initiate_private_state)
g.add_edge(n(initiate_private_state), n(placeholder_node))

g.add_node(placeholder_node)
g.add_edge(n(placeholder_node), n(placeholder_node2))

g.add_node(placeholder_node2)
g.add_edge(n(placeholder_node2), n(last_node))

g.add_node(last_node)
g.add_edge(n(last_node), END)

debugging_agent_graph = g.compile()

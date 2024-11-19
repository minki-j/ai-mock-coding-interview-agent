import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model

from . import prompts


class CodeFeedbackAgentPrivateState(BaseModel):
    interview_question: str = Field(default="")
    interview_solution: str = Field(default="")
    code_editor_state: str = Field(default="")

    debugging_result: str = Field(default="")
    assessment_result: str = Field(default="")


def initiate_private_state(state: OverallState) -> CodeFeedbackAgentPrivateState:
    return {
        "interview_question": state.interview_question,
        "interview_solution": state.interview_solution,
        "code_editor_state": state.code_editor_state,
    }


def assess_code_with_correct_solution(state: CodeFeedbackAgentPrivateState):
    print("\n>>> NODE: assess_code_with_correct_solution")

    response = (
        ChatPromptTemplate.from_template(prompts.ASSESSMENT_PROMPT) | chat_model
    ).invoke(
        {
            "interview_question": state.interview_question,
            "correct_solution": state.interview_solution,
            "user_solution": state.code_editor_state,
        }
    )

    return {
        "assessment_result": response.content,
    }


def generate_feedback(state: CodeFeedbackAgentPrivateState) -> OverallState:
    print("\n>>> NODE: generate_feedback")

    reply = (
        ChatPromptTemplate.from_template(prompts.FEEDBACK_PROMPT) | chat_model
    ).invoke(
        {
            "interview_question": state.interview_question,
            "user_solution": state.code_editor_state,
            "assessment": state.assessment_result,
        }
    )

    return {
        "message_from_interviewer": reply.content,
    }


g = StateGraph(OverallState)
g.add_edge(START, n(initiate_private_state))

g.add_node(initiate_private_state)
g.add_edge(n(initiate_private_state), n(assess_code_with_correct_solution))

g.add_node(assess_code_with_correct_solution)

g.add_edge(n(assess_code_with_correct_solution), "rendezvous")

g.add_node("rendezvous", RunnablePassthrough())
g.add_edge("rendezvous", n(generate_feedback))

g.add_node(generate_feedback)
g.add_edge(n(generate_feedback), END)

coding_step_graph = g.compile()

with open("./agents/graph_diagrams/coding_step_graph.png", "wb") as f:
    f.write(coding_step_graph.get_graph(xray=1).draw_mermaid_png())

import json
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState
from langchain_core.messages import AIMessage

from agents.llm_models import chat_model

from . import prompts


class CodeFeedbackAgentPrivateState(BaseModel):
    interview_question_md: str = Field(default="")
    user_approach: str = Field(default="")
    code_editor_state: str = Field(default="")

    assessment_result: str = Field(default="")


def initiate_private_state(state: OverallState) -> CodeFeedbackAgentPrivateState:
    if state.user_approach == "":
        user_approach = "\n".join(
            [json.dumps(approach) for approach in state.approaches]
        )
    else:
        user_approach = state.user_approach

    return {
        "interview_question_md": state.interview_question_md,
        "user_approach": user_approach,
        "code_editor_state": state.code_editor_state,
    }


def assess_code_with_correct_solution(state: CodeFeedbackAgentPrivateState):
    print("\n>>> NODE: assess_code_with_correct_solution")

    response = (
        ChatPromptTemplate.from_template(prompts.ASSESSMENT_PROMPT) | chat_model
    ).invoke(
        {
            "interview_question": state.interview_question_md,
            "correct_solution": state.user_approach,
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
            "interview_question": state.interview_question_md,
            "user_solution": state.code_editor_state,
            "assessment": state.assessment_result,
        }
    )

    return {
        "message_from_interviewer": reply.content,
        "messages": [reply],
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

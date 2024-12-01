import os
from varname import nameof as n
from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal
from langgraph.graph import START, END, StateGraph

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langgraph.checkpoint.memory import MemorySaver

from agents.state_schema import OverallState
from agents.llm_models import chat_model

from agents.subgraphs.main_stage import prompts

from agents.subgraphs.main_stage.coding.graph import coding_step_graph
from agents.subgraphs.main_stage.debugging.graph import debugging_step_graph
from agents.subgraphs.main_stage.algorithmic_analysis.graph import (
    algorithmic_analysis_step_graph,
)


def answer_general_question(state: OverallState):
    print("\n>>> NODE: answer_general_question")

    reply = (
        ChatPromptTemplate.from_template(prompts.DEFAULT_FEEDBACK_PROMPT) | chat_model
    ).invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type}: {message.content}"
                    for message in state.messages[-4:]  # last 4 messages
                ]
            ),
            "code_editor_state": state.code_editor_state,
            "interview_question": state.interview_question_md,
        }
    )

    return {
        "display_decision": "Answered the general question.",
        "message_from_interviewer": reply.content,
    }


def user_intent_classifier(state: OverallState):

    class Intent(Enum):
        GENERAL_QUESTION = "asking_general_question"
        CODE_FEEDBACK = "asking_for_code_feedback"

    class UserIntentResponse(BaseModel):
        rationale: str = Field(description="The rationale for the user's intent.")
        user_intent: Intent = Field(
            description="If the user's intent is 'asking_general_question', the user is asking a question about details of a library, API, or general programming knowledge that is not the complete solution to the problem.\n\nIf the user's intent is 'asking_for_code_feedback', the user wants to get feedback on their code solution."
        )

    response = (
        ChatPromptTemplate.from_template(prompts.USER_INTENT_CLASSIFIER_PROMPT)
        | chat_model.with_structured_output(UserIntentResponse)
    ).invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages[-4:]  # last 4 messages
                ]
            ),
        }
    )

    if response.user_intent == Intent.CODE_FEEDBACK:
        return n(display_user_intent_code_feedback)
    elif response.user_intent == Intent.GENERAL_QUESTION:
        return n(display_user_intent_general_question)
    else:
        raise ValueError(f"Invalid user intent: {response.user_intent}")


def display_user_intent_code_feedback(state: OverallState):
    print("\n>>> NODE: display_user_intent_code_feedback")
    return {
        "display_decision": "Identified that the user asked for code feedback.",
    }


def display_user_intent_general_question(state: OverallState):
    print("\n>>> NODE: display_user_intent_general_question")
    return {
        "display_decision": "Identified that the user asked a general question.",
    }


def main_stage_step_router(state: OverallState):
    print("\n>>> NODE: main_stage_step_router")
    if state.main_stage_step == "coding":
        return n(coding_step_graph)
    elif state.main_stage_step == "debugging":
        return n(debugging_step_graph)
    elif state.main_stage_step == "algorithmic_analysis":
        return n(algorithmic_analysis_step_graph)
    else:
        raise ValueError(f"Invalid main stage step: {state.main_stage_step}")


def should_move_to_next_step(state: OverallState):
    print("\n>>> NODE: should_move_to_next_step")

    class NextStepResponse(BaseModel):
        should_move_to_next_step: bool = Field(
            description="Whether to move to the next step or stay in the current step."
        )

    response = (
        ChatPromptTemplate.from_template(prompts.DECIDE_WHETHER_TO_MOVE_TO_NEXT_STEP)
        | chat_model.with_structured_output(NextStepResponse)
    ).invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages[-4:]
                ]
            ),
            "code_editor_state": state.code_editor_state,
            "current_step": state.main_stage_step,
        }
    )
    if response.should_move_to_next_step:
        if state.main_stage_step == "coding":
            return {
                "display_decision": "Concluded that you have finished coding.",
                "main_stage_step": "debugging",
            }
        elif state.main_stage_step == "debugging":
            return {
                "display_decision": "Concluded that you have finished debugging.",
                "main_stage_step": "algorithmic_analysis",
            }
        elif state.main_stage_step == "algorithmic_analysis":
            return {
                "display_decision": "Concluded that you have finished algorithmic analysis.",
                "stage": "assessment",
            }
    else:
        return {
            "display_decision": "Concluded that you might need more time for the current step.",
            "main_stage_step": state.main_stage_step,
        }


g = StateGraph(OverallState)

g.add_edge(START, n(user_intent_classifier))

g.add_node(n(user_intent_classifier), RunnablePassthrough())
g.add_conditional_edges(
    n(user_intent_classifier),
    user_intent_classifier,
    [n(display_user_intent_general_question), n(display_user_intent_code_feedback)],
)

g.add_node(display_user_intent_general_question)
g.add_edge(n(display_user_intent_general_question), n(answer_general_question))

g.add_node(display_user_intent_code_feedback)
g.add_edge(n(display_user_intent_code_feedback), n(main_stage_step_router))

g.add_node(n(main_stage_step_router), RunnablePassthrough())
g.add_conditional_edges(
    n(main_stage_step_router),
    main_stage_step_router,
    [
        n(coding_step_graph),
        n(debugging_step_graph),
        n(algorithmic_analysis_step_graph),
    ],
)

g.add_node(n(coding_step_graph), coding_step_graph)
g.add_edge(n(coding_step_graph), n(should_move_to_next_step))

g.add_node(n(debugging_step_graph), debugging_step_graph)
g.add_edge(n(debugging_step_graph), n(should_move_to_next_step))

g.add_node(n(algorithmic_analysis_step_graph), algorithmic_analysis_step_graph)
g.add_edge(n(algorithmic_analysis_step_graph), n(should_move_to_next_step))

g.add_node(n(answer_general_question), answer_general_question)
g.add_edge(n(answer_general_question), n(should_move_to_next_step))

g.add_node(n(should_move_to_next_step), should_move_to_next_step)
g.add_edge(n(should_move_to_next_step), END)

main_stage_graph = g.compile(
    checkpointer=MemorySaver(),
    interrupt_after=[
        n(display_user_intent_general_question),
        n(display_user_intent_code_feedback),
        n(answer_general_question),
        n(should_move_to_next_step),
    ],
)

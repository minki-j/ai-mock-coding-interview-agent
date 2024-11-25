import json
import os
from enum import Enum
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model
from agents.subgraphs.thought_process_stage.prompts import (
    default_system_message,
    IDENTIFY_USER_APPROACH,
    GIVE_APPROACH_SPEIFIC_HINT,
)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field


def is_user_approach_known(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: is_user_approach_known")
    if state.user_approach:
        return n(approach_based_reply)
    else:
        return n(general_reply)


def approach_based_reply(state: OverallState):
    print("\n>>> NODE: approach_based_reply")
    response = (
        ChatPromptTemplate.from_template(GIVE_APPROACH_SPEIFIC_HINT) | chat_model
    ).invoke(
        {
            "question": state.interview_question,
            "approach": f"{state.user_approach}",
            "conversation": state.stringify_messages(),
        }
    )

    return {
        "message_from_interviewer": response.content.strip("ai: "),
        "messages": [AIMessage(content=response.content.strip("ai: "))],
    }


def detect_user_approach(state: OverallState):
    print("\n>>> NODE: detect_user_approach")

    Approach = Enum(
        "Approach",
        {
            "UNKNOWN": "UNKNOWN",
            **{
                approach["title"]: approach["title"]
                for approach in state.interview_approaches
            },
        },
    )

    IdentifyUserApproachResponse = type(
        "IdentifyUserApproachResponse",
        (BaseModel,),
        {"__annotations__": {"approach": Approach}, "approach": Field()},
    )

    approach_enum = (
        (
            ChatPromptTemplate.from_template(IDENTIFY_USER_APPROACH)
            | chat_model.with_structured_output(IdentifyUserApproachResponse)
        )
        .invoke(
            {
                "question": state.interview_question,
                "approaches": state.interview_approaches,
                "conversation": state.stringify_messages(),
            }
        )
        .approach
    )

    user_approach_dict = next(
        (
            approach
            for approach in state.interview_approaches
            if approach["title"] == approach_enum.value
        ),
        None,
    )

    if user_approach_dict is None:
        return {"user_approach": "unknown"}

    return {"user_approach": json.dumps(user_approach_dict)}


def general_reply(state: OverallState):
    print("\n>>> NODE: general_reply")

    chain = (
        ChatPromptTemplate.from_messages(state.messages)
        | chat_model
        | StrOutputParser()
    )

    reply = chain.invoke({})

    return {
        "message_from_interviewer": reply,
        "messages": [AIMessage(content=reply)],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(detect_user_approach))

g.add_node(detect_user_approach)
g.add_edge(n(detect_user_approach), n(is_user_approach_known))

g.add_node(n(is_user_approach_known), RunnablePassthrough())
g.add_node(approach_based_reply)
g.add_conditional_edges(
    n(is_user_approach_known),
    is_user_approach_known,
    [n(approach_based_reply), n(general_reply)],
)

g.add_node(general_reply)
g.add_edge(n(general_reply), END)
g.add_edge(n(approach_based_reply), END)

thought_process_stage_graph = g.compile()

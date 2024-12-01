import json
import os
from enum import Enum
from varname import nameof as n

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model
from agents.subgraphs.thought_process_stage import prompts
from langchain_core.messages import AIMessage

from pydantic import BaseModel, Field


def is_user_approach_known(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: is_user_approach_known")
    if state.user_approach == "unknown":
        return n(general_reply)
    else:
        return n(approach_based_reply)

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
            ChatPromptTemplate.from_template(prompts.IDENTIFY_USER_APPROACH)
            | chat_model.with_structured_output(IdentifyUserApproachResponse)
        )
        .invoke(
            {
                "question": state.interview_question_md,
                "approaches": "\n\n".join(
                    [
                        f"## {approach['title']}\n{approach['approach']}"
                        for approach in state.interview_approaches
                    ]
                ),
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
        return {
            "display_decision": "Couldn't identify your approach yet.",
            "user_approach": "unknown",
        }

    return {
        "display_decision": f"Recognized your proposed approach as the  \"{user_approach_dict['title']}\".",
        "user_approach": json.dumps(user_approach_dict),
    }


def approach_based_reply(state: OverallState):
    print("\n>>> NODE: approach_based_reply")
    response = (
        ChatPromptTemplate.from_template(prompts.GIVE_APPROACH_SPEIFIC_HINT)
        | chat_model
    ).invoke(
        {
            "question": state.interview_question_md,
            "approach": f"{state.user_approach}",
            "conversation": state.stringify_messages(),
        }
    )

    return {
        "display_decision": "Generated a reply considering your approach.",
        "message_from_interviewer": response.content.strip("ai: "),
        "messages": [AIMessage(content=response.content.strip("ai: "))],
    }


def general_reply(state: OverallState):
    print("\n>>> NODE: general_reply")

    chain = (
        ChatPromptTemplate.from_messages(state.messages)
        | chat_model
        | StrOutputParser()
    )

    reply = chain.invoke({})

    return {
        "display_decision": "Completed writing a reply.",
        "message_from_interviewer": reply,
        "messages": [AIMessage(content=reply)],
    }


def is_thought_process_done(state: OverallState):
    print("\n>>> NODE: is_thought_process_done")

    class ClassifierResponse(BaseModel):
        rationale: str = Field(description="The rationale for the decision.")
        should_end_thought_process: bool = Field(
            description="Return True if the candidate has finished thinking about the problem or wants to move on to the actual interview stage, otherwise return False."
        )

    chain = ChatPromptTemplate.from_template(
        prompts.IS_THOUGHT_PROCESS_DONE
    ) | chat_model.with_structured_output(ClassifierResponse)

    stringified_messages = "\n\n".join(
        [
            f">>{message.type.upper()}: {message.content}"
            for message in state.messages[1:]
        ]
    )

    if chain.invoke({"messages": stringified_messages}).should_end_thought_process:
        return {
            "display_decision": "Concluded that you have provided sufficient thought process.",
            "stage": "main",
        }
    else:
        return {
            "display_decision": "Concluded that you might need more time for thought process.",
            "stage": "thought_process",
        }


g = StateGraph(OverallState)
g.add_edge(START, n(detect_user_approach))

g.add_node(detect_user_approach)
g.add_edge(n(detect_user_approach), n(is_user_approach_known))

g.add_node(n(is_user_approach_known), RunnablePassthrough())
g.add_conditional_edges(
    n(is_user_approach_known),
    is_user_approach_known,
    [n(approach_based_reply), n(general_reply)],
)

g.add_node(approach_based_reply)
g.add_edge(n(approach_based_reply), n(is_thought_process_done))

g.add_node(general_reply)
g.add_edge(n(general_reply), n(is_thought_process_done))

g.add_node(is_thought_process_done)
g.add_edge(n(is_thought_process_done), END)


thought_process_stage_graph = g.compile(
    checkpointer=MemorySaver(),
    interrupt_after=[
        n(detect_user_approach),
        n(approach_based_reply),
        n(general_reply),
        n(is_thought_process_done),
    ],
)

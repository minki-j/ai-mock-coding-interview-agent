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
from agents.subgraphs.thought_process_stage.prompts import default_system_message, IDENTIFY_USER_APPROACH, GIVE_APPROACH_SPEIFIC_HINT
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

    print(f"\n>>>NODE: {state.user_approach}")
    response = (
        ChatPromptTemplate.from_template(GIVE_APPROACH_SPEIFIC_HINT) | chat_model
    ).invoke(
        {
            "question": state.interview_question,
            "approach": f"{state.user_approach}",
            "conversation": state.stringify_messages()
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
        {
            "__annotations__": {"approach": Approach},
            "approach": Field()
        }
    )

    approach_enum = (
        ChatPromptTemplate.from_template(IDENTIFY_USER_APPROACH)
        | chat_model.with_structured_output(IdentifyUserApproachResponse)
    ).invoke(
        {
            "question": state.interview_question,
            "approaches": state.interview_approaches,
            "conversation": state.stringify_messages(),
        }
    ).approach

    user_approach_dict = next((approach for approach in state.interview_approaches if approach['title'] == approach_enum.value), None)

    if user_approach_dict is None:
        raise ValueError(f"Approach {approach_enum.value} not found in {state.interview_approaches}")

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


def is_greeting_finished(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: is_greeting_finished")
    if state.stage == "greeting":
        return n(greeting)
    else:
        return n(detect_user_approach)


def greeting(state: OverallState):
    print("\n>>> NODE: greeting")
    first_msg = f"Hello! {state.interviewee_name} How are you doing today?\n\n💡If you already know how the interview works, you can answer 'skip'.)"
    greeting_messages = [
        """Let me explain the structure of the interview. There are two parts:

1. Thought Process Phase: In this stage, you’ll walk me through how you would approach solving the problem.

2. Coding Phase: In this stage, you will implement your solution based on the approach discussed.

Does this make sense?""",
        """Great! Let's begin the thought process phase.

Please read the interview question above carefully, and explain how you would approach the problem. Feel free to ask clarifying questions at any point 😁""",
    ]

    if len(state.messages) == 0:
        greeting_msg = first_msg
        return {
            "message_from_interviewer": greeting_msg,
            "messages": [
                default_system_message(state.interview_question_md),
                AIMessage(content=greeting_msg),
            ],
        }
    else:
        if len(state.messages) > 1 and state.messages[-1].content.strip().lower() == "skip":
            greeting_msg_index = -1
            return {
                "message_from_interviewer": greeting_messages[greeting_msg_index],
                "messages": [AIMessage(content=greeting_messages[greeting_msg_index])],
                "greeting_msg_index": greeting_msg_index,
                "stage": "greeting" if greeting_msg_index < len(greeting_messages) and greeting_msg_index >= 0 else "thought_process",
        }

        class ContextualizedGreetingMessage(BaseModel):
            rationale: str = Field(description="The rationale for the decision.")
            should_use_predefined_reply: bool = Field(description="Return True if the predefined reply fits in the conversation. Otherwise, return False.")
            amended_predefined_reply: str = Field(description="Return the amended predefined reply if should_use_predefined_reply is True. Otherwise, return an empty string.")
            free_reply: str = Field(description="Return the free reply if should_use_predefined_reply is False. Otherwise, return an empty string.")

        chain = (
            ChatPromptTemplate.from_template(
                """
You just started interviewing a candidate for a software engineering role. There are three stages in this interview: greeting, thought process, and coding. You are currently in the greeting stage. You are going to greet the candidate and introduce how the interview will work. In thought process stage, you will ask the candidate to explain how they would approach solving the problem, and the candidate will answer through chat. In coding stage, the candidate will write code in the code editor that is shown in the right panel. The interview question is displayed above this chat panel.No 

---

Now you have to decide which option to use to reply to the candidate. Options are:slook 
{predefined_reply}

---

## conversation
{conversation}"""
            )
            | chat_model.with_structured_output(ContextualizedGreetingMessage)
        )

        stringified_messages = "\n\n".join(
            [f">>{message.type}: {message.content}" for message in state.messages[1:]]
        )
        
        response = chain.invoke(
            {
                "predefined_reply": greeting_messages[state.greeting_msg_index ],
                "conversation": stringified_messages,
            }
        )

        if response.should_use_predefined_reply:
            greeting_msg = response.amended_predefined_reply
            greeting_msg_index = state.greeting_msg_index + 1
        else:
            greeting_msg = response.free_reply
            greeting_msg_index = state.greeting_msg_index

        return {
            "message_from_interviewer": greeting_msg,
            "messages": [AIMessage(content=greeting_msg)],
            "greeting_msg_index": greeting_msg_index,
            "stage": "greeting" if greeting_msg_index < len(greeting_messages) else "thought_process",
        }


g = StateGraph(OverallState)
g.add_edge(START, n(is_greeting_finished))

g.add_node(n(is_greeting_finished), RunnablePassthrough())
g.add_conditional_edges(
    n(is_greeting_finished),
    is_greeting_finished,
    [n(greeting), n(detect_user_approach)],
)

g.add_node(detect_user_approach)
g.add_edge(n(detect_user_approach), n(is_user_approach_known))

g.add_node(n(is_user_approach_known), RunnablePassthrough())
g.add_node(approach_based_reply)
g.add_conditional_edges(n(is_user_approach_known), is_user_approach_known, [n(approach_based_reply), n(general_reply)])

g.add_node(greeting)
g.add_edge(n(greeting), END)

g.add_node(general_reply)
g.add_edge(n(general_reply), END)
g.add_edge(n(approach_based_reply), END)

thought_process_stage_graph = g.compile()
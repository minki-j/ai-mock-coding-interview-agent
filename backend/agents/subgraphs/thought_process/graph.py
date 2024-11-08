import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model
from agents.subgraphs.thought_process.prompts import default_system_message


def thought_process(state: OverallState):
    print("\n>>> NODE: thought_process")

    chain = (
        ChatPromptTemplate.from_messages(state.messages)
        | chat_model
        | StrOutputParser()
    )

    reply = chain.invoke({})

    return {
        "message_from_interviewer": reply,
        "messages": [reply],
    }


def is_first_message(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: is_first_message")
    if state.stage == "greeting":
        return n(greeting)
    else:
        return n(thought_process)


def greeting(state: OverallState):
    print("\n>>> NODE: greeting")
    first_message = f"Hello! {state.interviewee_name} How are you doing today?"
    explanation_list = [
        "First, let me explain the structure of the interview.\nThere are two steps: thought process and actual coding part. In the thought process stage, you will walk me through your thought process on how to solve the problem.\nDoes it make sense?",
        "Great! Let's begin.\nPlease read the interview question above carefully, and explain how you would approach the problem. Feel free to ask clarifying questions at any point.",
    ]

    if len(state.messages) == 0:
        default_greeting = first_message
        return {
            "message_from_interviewer": default_greeting,
            "messages": [
                default_system_message(state.interview_question),
                default_greeting,
            ],
        }
    else:
        chain = (
            ChatPromptTemplate.from_template(
                """
You are interviewing a candidate for a software engineering role. Amend the pre-defined reply to fit in the conversation. If it already fits, just return it as is. Only return the amended reply, nothing else such as "Here is the amended reply:".

---

predefined_reply: {predefined_reply}

conversation: {conversation}

---                                               

Important: Only return the amended reply, nothing else such as "Here is the amended reply:"."""
            )
            | chat_model
            | StrOutputParser()
        )
        stringified_messages = "\n".join(
            [f"{message.type}: {message.content}" for message in state.messages]
        )
        default_greeting = chain.invoke(
            {
                "predefined_reply": explanation_list[0],
                "conversation": stringified_messages,
            }
        )

        return {
            "message_from_interviewer": default_greeting,
            "messages": [default_greeting],
        }


g = StateGraph(OverallState)
g.add_edge(START, n(is_first_message))

g.add_conditional_edges(
    n(is_first_message), is_first_message, [(n(greeting), n(thought_process))]
)

g.add_node(greeting)
g.add_edge(n(greeting), END)

g.add_node(thought_process)
g.add_edge(n(thought_process), END)

thought_process_graph = g.compile()

import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model
from agents.subgraphs.thought_process.prompts import default_system_message
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field


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
    first_msg = f"Hello! {state.interviewee_name} How are you doing today?"
    greeting_messages = [
        "First, let me explain the structure of the interview.\nThere are two steps: thought process and actual coding part. In the thought process stage, you will walk me through your thought process on how to solve the problem.\nDoes it make sense?",
        "Great! Let's begin.\nPlease read the interview question above carefully, and explain how you would approach the problem. Feel free to ask clarifying questions at any point.",
    ]

    if len(state.messages) == 0:
        greeting_msg = first_msg
        return {
            "message_from_interviewer": greeting_msg,
            "messages": [
                default_system_message(state.interview_question),
                AIMessage(content=greeting_msg),
            ],
        }
    else:
        class ContextualizedGreetingMessage(BaseModel):
            should_use_predefined_reply: bool = Field(description="Return True if the predefined reply fits in the conversation. Otherwise, return False.")
            amended_predefined_reply: str = Field(description="Return the amended predefined reply if should_use_predefined_reply is True. Otherwise, return an empty string.")

        chain = (
            ChatPromptTemplate.from_template(
                """
You just started interviewing a candidate for a software engineering role. You have two options

Option 1. Use the predefined reply.
If the conversation flows as expected so that the predefined reply fits in the conversation, you can use it. However, the predefined reply may miss some reactions or tones. You can amend it to fit in the conversation.

Option 2. Ignore the predefined reply and reply freely.
Sometimes the interviewee might ask a question that is not covered in the predefined reply. Or the conversation might go in a different direction. In that case, you should ignore the predefined reply and reply freely. However, if the conversation is derailed too much, you should gently guide the conversation back to the predefined reply.

---

predefined_reply: {predefined_reply}

conversation: {conversation}"""
            )
            | chat_model.with_structured_output(ContextualizedGreetingMessage)
        )

        stringified_messages = "\n".join(
            [f"{message.type}: {message.content}" for message in state.messages[1:]]
        )

        greeting_msg = chain.invoke(
            {
                "predefined_replies": greeting_messages[state.greeting_msg_index],
                "conversation": stringified_messages,
            }
        )

        return {
            "message_from_interviewer": greeting_msg,
            "messages": [AIMessage(content=greeting_msg)],
        }


g = StateGraph(OverallState)
g.add_edge(START, n(is_first_message))

g.add_node(n(is_first_message), RunnablePassthrough())
g.add_conditional_edges(
    n(is_first_message),
    is_first_message,
    [n(greeting), n(thought_process)],
)

g.add_node(greeting)
g.add_edge(n(greeting), END)

g.add_node(thought_process)
g.add_edge(n(thought_process), END)

thought_process_graph = g.compile()

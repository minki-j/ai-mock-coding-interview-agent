import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model
from agents.subgraphs.thought_process_stage.prompts import default_system_message
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
        "messages": [AIMessage(content=reply)],
    }


def is_greeting_finished(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: is_greeting_finished")
    if state.stage == "greeting":
        return n(greeting)
    else:
        return n(thought_process)


def greeting(state: OverallState):
    print("\n>>> NODE: greeting")
    first_msg = f"Hello! {state.interviewee_name} How are you doing today?"
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
                "predefined_reply": greeting_messages[state.greeting_msg_index],
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
    [n(greeting), n(thought_process)],
)

g.add_node(greeting)
g.add_edge(n(greeting), END)

g.add_node(thought_process)
g.add_edge(n(thought_process), END)

thought_process_stage_graph = g.compile()
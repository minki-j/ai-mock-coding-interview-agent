import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState
from langgraph.checkpoint.memory import MemorySaver


from agents.llm_models import chat_model


def generate_feedback(state: OverallState) -> OverallState:
    print("\n>>> NODE: generate_feedback")

    reply = (
        ChatPromptTemplate.from_template(
            """
You are interviewing a candidate for a software engineering role. The candidate has written a solution to a problem. Now, it's time to debug the solution. In the debugging step, you can ask the candidate to come up with more edge cases and address them.
                                         
---

Interview question:
{interview_question}

---

Current conversation:
{messages}

---

The code that the candidate wrote:
{code_editor_state}

Reply to the candidate's last message.
"""
        )
        | chat_model
    ).invoke(
        {
            "interview_question": state.interview_question_md,
            "code_editor_state": state.code_editor_state,
            "messages": "\n\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages[-4:]
                ]
            ),
        }
    )

    return {
        "display_decision": "Generated feedback for your debugging.",
        "message_from_interviewer": reply.content,
        "messages": [reply],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_feedback))

g.add_node(generate_feedback)
g.add_edge(n(generate_feedback), END)

debugging_step_graph = g.compile(checkpointer=MemorySaver(), interrupt_after=[n(generate_feedback)])

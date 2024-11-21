import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model


def generate_feedback(state: OverallState) -> OverallState:
    print("\n>>> NODE: generate_feedback")

    reply = (
        ChatPromptTemplate.from_template(
            """
You are interviewing a candidate for a software engineering role. The candidate has written a solution to a problem. Now, it's time to analyze the time and space complexity of their solution.
                                         
---

Interview question:
{interview_question}

---

Current conversation:
{messages}

---

The code that the candidate wrote:
{code_editor_state}
"""
        )
        | chat_model
    ).invoke(
        {
            "interview_question": state.interview_question,
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
        "message_from_interviewer": reply.content,
        "messages": [reply],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_feedback))

g.add_node(generate_feedback)
g.add_edge(n(generate_feedback), END)

algorithmic_analysis_step_graph = g.compile()

with open("./agents/graph_diagrams/algorithmic_analysis_step_graph.png", "wb") as f:
    f.write(algorithmic_analysis_step_graph.get_graph(xray=1).draw_mermaid_png())

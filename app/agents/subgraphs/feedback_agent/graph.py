import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState


def generate_feedback(state: OverallState):
    print("\n>>> NODE: generate_feedback")

    return {"message_from_interviewer": "test feedback message"}


g = StateGraph(OverallState)
g.add_edge(START, n(generate_feedback))

g.add_node(generate_feedback)
g.add_edge(n(generate_feedback), END)

feedback_agent_graph = g.compile()

import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState


def generate_thought_process(state: OverallState):
    return {"message_from_interviewer": "test thought process message"}


g = StateGraph(OverallState)
g.add_edge(START, n(generate_thought_process))

g.add_node(generate_thought_process)
g.add_edge(n(generate_thought_process), END)

thought_process_graph = g.compile()

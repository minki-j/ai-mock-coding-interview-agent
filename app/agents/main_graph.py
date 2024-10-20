import os
import sqlite3
from varname import nameof as n

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState, InputState, OutputState

from app.agents.subgraphs.generate_question.graph import generate_question_graph
from app.agents.subgraphs.feedback_agent.graph import feedback_agent_graph
from app.agents.subgraphs.thought_process.graph import thought_process_graph

g = StateGraph(OverallState, input=InputState, output=OutputState)

g.add_edge(START, "check_if_question_generated")

g.add_node("check_if_question_generated", RunnablePassthrough())
g.add_conditional_edges(
    "check_if_question_generated",
    lambda x: (
        n(generate_question_graph)
        if not x.is_question_generated
        else "check_if_thought_process_stage"
    ),
    [n(generate_question_graph), "check_if_thought_process_stage"],
)

g.add_node(n(generate_question_graph), generate_question_graph)
g.add_edge(n(generate_question_graph), END)

g.add_node("check_if_thought_process_stage", RunnablePassthrough())
g.add_conditional_edges(
    "check_if_thought_process_stage",
    lambda x: n(thought_process_graph) if x.is_thought_process_stage else n(feedback_agent_graph),
    [n(feedback_agent_graph), n(thought_process_graph)],
)

g.add_node(n(thought_process_graph), thought_process_graph)
g.add_edge(n(thought_process_graph), END)

g.add_node(n(feedback_agent_graph), feedback_agent_graph)
g.add_edge(n(feedback_agent_graph), END)


os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory)

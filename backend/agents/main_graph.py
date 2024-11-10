import os
import sqlite3
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.state_schema import OverallState, InputState, OutputState

from agents.llm_models import chat_model
from agents.subgraphs.feedback_agent.graph import feedback_agent_graph
from agents.subgraphs.thought_process.graph import thought_process_graph
from agents.subgraphs.assessment_agent.graph import assessment_agent_graph


def stage_router(state: OverallState) -> bool:
    class ClassifierResponse(BaseModel):
        rationale: str = Field(description="The rationale for the decision.")
        should_end_thought_process: bool = Field(description="Return True if the candidate has finished thinking about the problem or wants to move on to the actual interview stage, otherwise return False.")

    print("\n>>> NODE: stage_router")
    if state.stage == "coding":
        return n(feedback_agent_graph)

    if state.stage == "assessment":
        return n(assessment_agent_graph)

    if len(state.messages[1:]) < 2:
        return n(thought_process_graph)

    chain = (
        ChatPromptTemplate.from_template(
            """
You are interviewing a candidate for a software engineering role.There are two stages of the interview. A) Thought process stage: The candidate is thinking out loud about the problem. B) Actual coding stage: The candidate is writing code to solve the problem.
The candidate is currently in the thought process stage. You need to decide if the candidate has provided enough thought process for the problem and can move on to the actual interview stage.

----

Important rules:
1. Even though the candiate didn't provide enough thought process, if the candidate wants to move on to the actual interview stage, you should let them.
2. Criteria for enough thought process:
    - The candidate understood the problem correctly
    - The candidate has some ideas on how to solve the problem
    - The candidate considered at least one edge case

----

Here is the current conversation:
{messages}
"""
        )
        | chat_model.with_structured_output(ClassifierResponse)
    )

    stringified_messages = "\n".join([f">>{message.type.upper()}: {message.content}" for message in state.messages[1:]])

    if not chain.invoke({"messages": stringified_messages}).should_end_thought_process:
        return n(thought_process_graph)
    else:
        return n(feedback_agent_graph)

g = StateGraph(OverallState, input=InputState, output=OutputState)
g.add_edge(START, n(stage_router))

g.add_node(n(stage_router), RunnablePassthrough())
g.add_conditional_edges(
    n(stage_router),
    stage_router,
    [n(feedback_agent_graph), n(thought_process_graph), n(assessment_agent_graph)],
)

g.add_node(n(thought_process_graph), thought_process_graph)
g.add_edge(n(thought_process_graph), "end_of_loop")

g.add_node(n(feedback_agent_graph), feedback_agent_graph)
g.add_edge(n(feedback_agent_graph), "end_of_loop")

g.add_node(n(assessment_agent_graph), assessment_agent_graph)
g.add_edge(n(assessment_agent_graph), "end_of_loop")

g.add_node("end_of_loop", RunnablePassthrough())
g.add_edge("end_of_loop", n(stage_router))

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["end_of_loop"])

with open("./agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())

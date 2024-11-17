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
from agents.subgraphs.coding_stage.graph import coding_stage_graph
from agents.subgraphs.thought_process_stage.graph import thought_process_stage_graph
from agents.subgraphs.final_assessment_stage.graph import final_assessment_stage_graph


def stage_router(state: OverallState) -> bool:
    print("\n>>> NODE: stage_router")

    class ClassifierResponse(BaseModel):
        rationale: str = Field(description="The rationale for the decision.")
        should_end_thought_process: bool = Field(description="Return True if the candidate has finished thinking about the problem or wants to move on to the actual interview stage, otherwise return False.")

    if state.stage == "greeting":
        return n(thought_process_stage_graph)

    if state.stage == "coding":
        return n(coding_stage_graph)

    if state.stage == "assessment":
        return n(final_assessment_stage_graph)

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

    stringified_messages = "\n\n".join(
        [
            f">>{message.type.upper()}: {message.content}"
            for message in state.messages[1:]
        ]
    )

    if not chain.invoke({"messages": stringified_messages}).should_end_thought_process:
        return n(thought_process_stage_graph)
    else:
        return n(coding_stage_graph)

g = StateGraph(OverallState, input=InputState, output=OutputState)
g.add_edge(START, n(stage_router))

g.add_node(n(stage_router), RunnablePassthrough())
g.add_conditional_edges(
    n(stage_router),
    stage_router,
    [n(coding_stage_graph), n(thought_process_stage_graph), n(final_assessment_stage_graph)],
)

g.add_node(n(thought_process_stage_graph), thought_process_stage_graph)
g.add_edge(n(thought_process_stage_graph), "end_of_loop")

g.add_node(n(coding_stage_graph), coding_stage_graph)
g.add_edge(n(coding_stage_graph), "end_of_loop")

g.add_node(n(final_assessment_stage_graph), final_assessment_stage_graph)
g.add_edge(n(final_assessment_stage_graph), "end_of_loop")

g.add_node("end_of_loop", RunnablePassthrough())
g.add_edge("end_of_loop", n(stage_router))

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["end_of_loop"])

with open("./agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=1).draw_mermaid_png())

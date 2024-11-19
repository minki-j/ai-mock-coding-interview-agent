import os
import sqlite3
from varname import nameof as n
from pydantic import BaseModel, Field
import asyncio

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


from agents.state_schema import OverallState, InputState, OutputState

from agents.llm_models import chat_model
from agents.subgraphs.main_stage.graph import main_stage_graph
from agents.subgraphs.thought_process_stage.graph import thought_process_stage_graph
from agents.subgraphs.final_assessment_stage.graph import final_assessment_stage_graph

from agents import prompts


def stage_router(state: OverallState) -> bool:
    print("\n>>> NODE: stage_router")

    if state.stage == "greeting":
        return n(thought_process_stage_graph)

    if state.stage == "main":
        return n(main_stage_graph)

    if state.stage == "assessment":
        return n(final_assessment_stage_graph)

    class ClassifierResponse(BaseModel):
        rationale: str = Field(description="The rationale for the decision.")
        should_end_thought_process: bool = Field(
            description="Return True if the candidate has finished thinking about the problem or wants to move on to the actual interview stage, otherwise return False."
        )

    chain = ChatPromptTemplate.from_template(
        prompts.USER_INTENT_CLASSIFIER_PROMPT
    ) | chat_model.with_structured_output(ClassifierResponse)

    stringified_messages = "\n\n".join(
        [
            f">>{message.type.upper()}: {message.content}"
            for message in state.messages[1:]
        ]
    )

    if chain.invoke({"messages": stringified_messages}).should_end_thought_process:
        return n(initiate_main_stage)
    else:
        return n(thought_process_stage_graph)


def initiate_main_stage(state: OverallState) -> OverallState:
    print("\n>>> NODE: initiate_main_stage")

    messages_for_first_reply = "\n\n".join(
        [
            f">>{message.type.upper()}: {message.content}"
            for message in state.messages[1:]
        ]
    )

    messages_for_thought_process_summary = "\n\n".join(
        [f">>{message.type.upper()}: {message.content}" for message in state.messages]
    )

    def prepare_first_reply_input(inputs):
        return {"messages": messages_for_first_reply}

    def prepare_thought_process_input(inputs):
        return {"messages": messages_for_thought_process_summary}

    first_reply_chain = (
        ChatPromptTemplate.from_template(prompts.FIRST_REPLY_PROMPT)
        | chat_model
        | StrOutputParser()
    )

    thought_process_chain = (
        ChatPromptTemplate.from_template(prompts.THOUGHT_PROCESS_SUMMARY_PROMPT)
        | chat_model
        | StrOutputParser()
    )

    parallel_chains = RunnableParallel(
        first_reply=RunnableLambda(prepare_first_reply_input) | first_reply_chain,
        thought_process_summary=RunnableLambda(prepare_thought_process_input)
        | thought_process_chain,
    )

    results = parallel_chains.invoke({})

    return {
        "stage": "main",
        "main_stage_step": "coding",
        "message_from_interviewer": results["first_reply"],
        "messages": [AIMessage(content=results["first_reply"])],
        "thought_process_summary": results["thought_process_summary"],
    }


g = StateGraph(OverallState, input=InputState, output=OutputState)
g.add_edge(START, n(stage_router))

g.add_node(n(stage_router), RunnablePassthrough())
g.add_conditional_edges(
    n(stage_router),
    stage_router,
    [
        n(main_stage_graph),
        n(thought_process_stage_graph),
        n(final_assessment_stage_graph),
        n(initiate_main_stage),
    ],
)

g.add_node(n(thought_process_stage_graph), thought_process_stage_graph)
g.add_edge(n(thought_process_stage_graph), "end_of_loop")

g.add_node(initiate_main_stage)
g.add_edge(n(initiate_main_stage), "end_of_loop")

g.add_node(n(main_stage_graph), main_stage_graph)
g.add_edge(n(main_stage_graph), "end_of_loop")

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

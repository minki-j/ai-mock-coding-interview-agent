import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model
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


g = StateGraph(OverallState)
g.add_edge(START, n(thought_process))

g.add_node(thought_process)
g.add_edge(n(thought_process), END)

thought_process_stage_graph = g.compile()
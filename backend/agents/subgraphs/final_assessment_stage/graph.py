import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.state_schema import OverallState

from agents.llm_models import chat_model

g = StateGraph(OverallState)
g.add_edge(START, "start")
g.add_node(
    "start",
    lambda _: {
        "message_from_interviewer": "It seems like we've reached the end of the interview. Do you want to see the final assessment?"
    },
)
g.add_edge("start", END)

final_assessment_stage_graph = g.compile()

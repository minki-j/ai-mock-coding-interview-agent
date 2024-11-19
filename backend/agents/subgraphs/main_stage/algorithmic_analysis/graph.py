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
g.add_node("start", RunnablePassthrough())
g.add_edge("start", END)

algorithmic_analysis_step_graph = g.compile()

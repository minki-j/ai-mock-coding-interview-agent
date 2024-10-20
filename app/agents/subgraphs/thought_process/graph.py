import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.state_schema import OverallState

from app.agents.llm_models import chat_model_small


def generate_thought_process(state: OverallState):
    print("\n>>> NODE: generate_thought_process")

    chain = (
        ChatPromptTemplate.from_messages(state.messages)
        | chat_model_small
    )

    response = chain.invoke({}) 

    return {
        "message_from_interviewer": response.content,
        "messages": [response],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_thought_process))

g.add_node(generate_thought_process)
g.add_edge(n(generate_thought_process), END)

thought_process_graph = g.compile()

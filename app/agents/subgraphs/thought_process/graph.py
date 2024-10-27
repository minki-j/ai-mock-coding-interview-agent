import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.state_schema import OverallState

from app.agents.llm_models import chat_model
from app.agents.subgraphs.thought_process.prompts import default_system_message


def generate_thought_process(state: OverallState):
    print("\n>>> NODE: generate_thought_process")

    messages = state.messages
    if len(messages) == 0:
        messages = default_system_message(state.interview_question)

    chain = ChatPromptTemplate.from_messages(messages) | chat_model

    response = chain.invoke({})

    return {
        "message_from_interviewer": response.content,
        "messages": [*messages, response],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_thought_process))

g.add_node(generate_thought_process)
g.add_edge(n(generate_thought_process), END)

thought_process_graph = g.compile()

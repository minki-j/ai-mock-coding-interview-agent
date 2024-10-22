import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState
from app.agents.llm_models import chat_model_small

from app.agents.subgraphs.feedback_agent import prompts

def generate_feedback(state: OverallState):
    print("\n>>> NODE: generate_feedback")

    chain =  ChatPromptTemplate.from_template(prompts.ASSESSMENT_PROMPT) | chat_model_small
    
    response = chain.invoke({
            'question': state.interview_question,
            'correct_solution': state.interview_solution,
            'user_solution': state.messages[-1]
        })

    chain =  ChatPromptTemplate.from_template(prompts.FEEDBACK_PROMPT) | chat_model_small

    response = chain.invoke({
            'question': state.interview_question,
            'user_solution': state.messages[-1],
            'feedback': response.content
        })

    return {
        "message_from_interviewer": response.content,
        "messages": [response],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_feedback))

g.add_node(generate_feedback)
g.add_edge(n(generate_feedback), END)

feedback_agent_graph = g.compile()

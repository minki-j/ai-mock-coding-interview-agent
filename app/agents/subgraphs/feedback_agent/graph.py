import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState
from app.agents.llm_models import chat_model

from app.agents.subgraphs.feedback_agent import prompts
from app.agents.subgraphs.code_interpreter.graph import code_interpreter_graph

def generate_feedback(state: OverallState):
    print("\n>>> NODE: generate_feedback")

    # Execute the code
    code_execution_result = code_interpreter_graph.invoke(state)

    chain = ChatPromptTemplate.from_template(prompts.ASSESSMENT_PROMPT) | chat_model

    assessment_response = chain.invoke({
        'question': state.interview_question,
        'correct_solution': state.interview_solution,
        'user_solution': state.code_editor_state,
        'execution_result': code_execution_result['code_execution_result']
    })

    chain = ChatPromptTemplate.from_template(prompts.FEEDBACK_PROMPT) | chat_model

    feedback_response = chain.invoke(
        {
            "question": state.interview_question,
            "user_solution": state.code_editor_state,
            "assessment": assessment_response.content,
            "execution_result": code_execution_result['code_execution_result']
        }
    )

    return {
        "message_from_interviewer": feedback_response.content,
        "messages": [feedback_response],
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_feedback))

g.add_node(generate_feedback)
g.add_edge(n(generate_feedback), END)

feedback_agent_graph = g.compile()
